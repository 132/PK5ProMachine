//
// Created by bialan132 on 5/9/18.
//


#include <ripple/app/tx/impl/LogTransaction.h>
#include <ripple/app/tx/impl/Transactor.h>
#include <ripple/app/ledger/OrderBookDB.h>
#include <ripple/app/paths/Flow.h>
#include <ripple/ledger/CashDiff.h>
#include <ripple/ledger/PaymentSandbox.h>
#include <ripple/protocol/Feature.h>
#include <ripple/protocol/st.h>
#include <ripple/protocol/Quality.h>
#include <ripple/beast/utility/WrappedSink.h>

namespace ripple {
    TER
    LogTransaction::preflight (PreflightContext const& ctx)
    {
        if (! ctx.rules.enabled (featureChecks))
            return temDISABLED;

        TER const ret {preflight1 (ctx)};

        if (! isTesSuccess (ret))
            return ret;

        if (ctx.tx.getFlags() & tfUniversalMask)
        {
            // There are no flags (other than universal) for CreateCheck yet.
            JLOG(ctx.j.warn()) << "Malformed transaction: Invalid flags set.";
            return temINVALID_FLAG;
        }
        if (ctx.tx[sfAccount] == ctx.tx[sfDestination])
        {
            // They wrote a check to themselves.
            JLOG(ctx.j.warn()) << "Malformed transaction: Check to self.";
            return temREDUNDANT;
        }

        if (auto const optExpiry = ctx.tx[~sfExpiration])
        {
            if (*optExpiry == 0)
            {
                JLOG(ctx.j.warn()) << "Malformed transaction: bad expiration";
                return temBAD_EXPIRATION;
            }
        }

        return preflight2 (ctx);
    }


    TER
    LogTransaction::preclaim (PreclaimContext const& ctx)
    {
        auto const id = ctx.tx[sfAccount];

        std::uint32_t const uTxFlags = ctx.tx.getFlags();

        auto const sle = ctx.view.read(keylet::account(id));

        std::uint32_t const uFlagsIn = sle->getFieldU32(sfFlags);

        std::uint32_t const uSetFlag = ctx.tx.getFieldU32(sfSetFlag);

        // legacy AccountSet flags
        bool bSetRequireAuth = (uTxFlags & tfRequireAuth) || (uSetFlag == asfRequireAuth);

        //
        // RequireAuth
        //
        if (bSetRequireAuth && !(uFlagsIn & lsfRequireAuth))
        {
            if (!dirIsEmpty(ctx.view,
                            keylet::ownerDir(id)))
            {
                JLOG(ctx.j.trace()) << "Retry: Owner directory not empty.";
                return (ctx.flags & tapRETRY) ? terOWNERS : tecOWNERS;
            }
        }
        return tesSUCCESS;
    }

    TER
    LogTransaction::doApply ()
    {

        // This is the ledger view that we work against. Transactions are applied
        // as we go on processing transactions.
        Sandbox sb (&ctx_.view());

        // This is a ledger with just the fees paid and any unfunded or expired
        // offers we encounter removed. It's used when handling Fill-or-Kill offers,
        // if the order isn't going to be placed, to avoid wasting the work we did.
        Sandbox sbCancel (&ctx_.view());

        auto const result = applyGuts(sb, sbCancel);
        if (result.second)
            sb.apply(ctx_.rawView());
        else
            sbCancel.apply(ctx_.rawView());
        return result.first;
    }

    void LogTransaction::preCompute(){

    }

    std::pair<TER, bool>
    LogTransaction::applyGuts (Sandbox& sb, Sandbox& sbCancel)
    {
        std::uint32_t const uTxFlags = ctx_.tx.getFlags ();

        bool const bPassive (uTxFlags & tfPassive);
        bool const bImmediateOrCancel (uTxFlags & tfImmediateOrCancel);
        bool const bFillOrKill (uTxFlags & tfFillOrKill);
        bool const bSell (uTxFlags & tfSell);

        auto saTakerPays = ctx_.tx[sfTakerPays];
        auto saTakerGets = ctx_.tx[sfTakerGets];

        auto const cancelSequence = ctx_.tx[~sfOfferSequence];

        // FIXME understand why we use SequenceNext instead of current transaction
        //       sequence to determine the transaction. Why is the offer sequence
        //       number insufficient?
        auto const uSequence = ctx_.tx.getSequence ();

        // This is the original rate of the offer, and is the rate at which
        // it will be placed, even if crossing offers change the amounts that
        // end up on the books.
        auto uRate = getRate (saTakerGets, saTakerPays);

        auto viewJ = ctx_.app.journal("View");

        auto result = tesSUCCESS;

        // Process a cancellation request that's passed along with an offer.
        if (cancelSequence)
        {
            auto const sleCancel = sb.peek(
                    keylet::offer(account_, *cancelSequence));

            // It's not an error to not find the offer to cancel: it might have
            // been consumed or removed. If it is found, however, it's an error
            // to fail to delete it.
            if (sleCancel)
            {
                JLOG(j_.debug()) << "Create cancels order " << *cancelSequence;
                result = offerDelete (sb, sleCancel, viewJ);
            }
        }

        auto const expiration = ctx_.tx[~sfExpiration];
        using d = NetClock::duration;
        using tp = NetClock::time_point;

        // Expiration is defined in terms of the close time of the parent ledger,
        // because we definitively know the time that it closed but we do not
        // know the closing time of the ledger that is under construction.
        if (expiration &&
            (ctx_.view().parentCloseTime() >= tp{d{*expiration}}))
        {
            // If the offer has expired, the transaction has successfully
            // done nothing, so short circuit from here.
            //
            // The return code change is attached to featureChecks as a convenience.
            // The change is not big enough to deserve its own amendment.
            TER const ter {ctx_.view().rules().enabled(
                    featureChecks) ? tecEXPIRED : tesSUCCESS};
            return{ ter, true };
        }

        bool const bOpenLedger = ctx_.view().open();
        bool crossed = false;

        if (result == tesSUCCESS)
        {
            // If a tick size applies, round the offer to the tick size
            auto const& uPaysIssuerID = saTakerPays.getIssuer ();
            auto const& uGetsIssuerID = saTakerGets.getIssuer ();

            std::uint8_t uTickSize = Quality::maxTickSize;
            if (!isXRP (uPaysIssuerID))
            {
                auto const sle =
                        sb.read(keylet::account(uPaysIssuerID));
                if (sle && sle->isFieldPresent (sfTickSize))
                    uTickSize = std::min (uTickSize,
                                          (*sle)[sfTickSize]);
            }
            if (!isXRP (uGetsIssuerID))
            {
                auto const sle =
                        sb.read(keylet::account(uGetsIssuerID));
                if (sle && sle->isFieldPresent (sfTickSize))
                    uTickSize = std::min (uTickSize,
                                          (*sle)[sfTickSize]);
            }
            if (uTickSize < Quality::maxTickSize)
            {
                auto const rate =
                        Quality{saTakerGets, saTakerPays}.round
                                (uTickSize).rate();

                // We round the side that's not exact,
                // just as if the offer happened to execute
                // at a slightly better (for the placer) rate
                if (bSell)
                {
                    // this is a sell, round taker pays
                    saTakerPays = multiply (
                            saTakerGets, rate, saTakerPays.issue());
                }
                else
                {
                    // this is a buy, round taker gets
                    saTakerGets = divide (
                            saTakerPays, rate, saTakerGets.issue());
                }
                if (! saTakerGets || ! saTakerPays)
                {
                    JLOG (j_.debug()) <<
                                      "Offer rounded to zero";
                    return { result, true };
                }

                uRate = getRate (saTakerGets, saTakerPays);
            }

            // We reverse pays and gets because during crossing we are taking.
            Amounts const takerAmount (saTakerGets, saTakerPays);

            // The amount of the offer that is unfilled after crossing has been
            // performed. It may be equal to the original amount (didn't cross),
            // empty (fully crossed), or something in-between.
            Amounts place_offer;

            JLOG(j_.debug()) << "Attempting cross: " <<
                             to_string (takerAmount.in.issue ()) << " -> " <<
                             to_string (takerAmount.out.issue ());

/*Tri Need to modify           if (auto stream = j_.trace())
            {
                stream << "   mode: " <<
                       (bPassive ? "passive " : "") <<
                       (bSell ? "sell" : "buy");
                stream <<"     in: " << format_amount (takerAmount.in);
                stream << "    out: " << format_amount (takerAmount.out);
            }

            std::tie(result, place_offer) = cross (sb, sbCancel, takerAmount);
*/
            // We expect the implementation of cross to succeed
            // or give a tec.
            assert(result == tesSUCCESS || isTecClaim(result));
/*
Tri Need to modify
            if (auto stream = j_.trace())
            {
                stream << "Cross result: " << transToken (result);
                stream << "     in: " << format_amount (place_offer.in);
                stream << "    out: " << format_amount (place_offer.out);
            }
*/

            if (result == tecFAILED_PROCESSING && bOpenLedger)
                result = telFAILED_PROCESSING;

            if (result != tesSUCCESS)
            {
                JLOG (j_.debug()) << "final result: " << transToken (result);
                return { result, true };
            }

            assert (saTakerGets.issue () == place_offer.in.issue ());
            assert (saTakerPays.issue () == place_offer.out.issue ());

            if (takerAmount != place_offer)
                crossed = true;

            // The offer that we need to place after offer crossing should
            // never be negative. If it is, something went very very wrong.

/*Tri Need to modify
            if (place_offer.in < zero || place_offer.out < zero)
            {
                JLOG(j_.fatal()) << "Cross left offer negative!" <<
                                 "     in: " << format_amount (place_offer.in) <<
                                 "    out: " << format_amount (place_offer.out);
                return { tefINTERNAL, true };
            }
*/

            if (place_offer.in == zero || place_offer.out == zero)
            {
                JLOG(j_.debug()) << "Offer fully crossed!";
                return { result, true };
            }

            // We now need to adjust the offer to reflect the amount left after
            // crossing. We reverse in and out here, since during crossing we
            // were the taker.
            saTakerPays = place_offer.out;
            saTakerGets = place_offer.in;
        }

        assert (saTakerPays > zero && saTakerGets > zero);

        if (result != tesSUCCESS)
        {
            JLOG (j_.debug()) << "final result: " << transToken (result);
            return { result, true };
        }

        if (auto stream = j_.trace())
        {
            stream << "Place" << (crossed ? " remaining " : " ") << "offer:";
            stream << "    Pays: " << saTakerPays.getFullText ();
            stream << "    Gets: " << saTakerGets.getFullText ();
        }

        // For 'fill or kill' offers, failure to fully cross means that the
        // entire operation should be aborted, with only fees paid.
        if (bFillOrKill)
        {
            JLOG (j_.trace()) << "Fill or Kill: offer killed";
            return { tesSUCCESS, false };
        }

        // For 'immediate or cancel' offers, the amount remaining doesn't get
        // placed - it gets cancelled and the operation succeeds.
        if (bImmediateOrCancel)
        {
            JLOG (j_.trace()) << "Immediate or cancel: offer cancelled";
            return { tesSUCCESS, true };
        }

        auto const sleCreator = sb.peek (keylet::account(account_));
        {
            XRPAmount reserve = ctx_.view().fees().accountReserve(
                    sleCreator->getFieldU32 (sfOwnerCount) + 1);

            if (mPriorBalance < reserve)
            {
                // If we are here, the signing account had an insufficient reserve
                // *prior* to our processing. If something actually crossed, then
                // we allow this; otherwise, we just claim a fee.
                if (!crossed)
                    result = tecINSUF_RESERVE_OFFER;

                if (result != tesSUCCESS)
                {
                    JLOG (j_.debug()) <<
                                      "final result: " << transToken (result);
                }

                return { result, true };
            }
        }

        // We need to place the remainder of the offer into its order book.
        auto const offer_index = getOfferIndex (account_, uSequence);

        // Add offer to owner's directory.
        auto const ownerNode = dirAdd(sb, keylet::ownerDir (account_),
                                      offer_index, false, describeOwnerDir (account_), viewJ);

        if (!ownerNode)
        {
            JLOG (j_.debug()) <<
                              "final result: failed to add offer to owner's directory";
            return { tecDIR_FULL, true };
        }

        // Update owner count.
        adjustOwnerCount(sb, sleCreator, 1, viewJ);

        JLOG (j_.trace()) <<
                          "adding to book: " << to_string (saTakerPays.issue ()) <<
                          " : " << to_string (saTakerGets.issue ());

        Book const book { saTakerPays.issue(), saTakerGets.issue() };

        // Add offer to order book, using the original rate
        // before any crossing occured.
        auto dir = keylet::quality (keylet::book (book), uRate);
        bool const bookExisted = static_cast<bool>(sb.peek (dir));

        auto const bookNode = dirAdd (sb, dir, offer_index, true,
                                      [&](SLE::ref sle)
                                      {
                                          sle->setFieldH160 (sfTakerPaysCurrency,
                                                             saTakerPays.issue().currency);
                                          sle->setFieldH160 (sfTakerPaysIssuer,
                                                             saTakerPays.issue().account);
                                          sle->setFieldH160 (sfTakerGetsCurrency,
                                                             saTakerGets.issue().currency);
                                          sle->setFieldH160 (sfTakerGetsIssuer,
                                                             saTakerGets.issue().account);
                                          sle->setFieldU64 (sfExchangeRate, uRate);
                                      }, viewJ);

        if (!bookNode)
        {
            JLOG (j_.debug()) <<
                              "final result: failed to add offer to book";
            return { tecDIR_FULL, true };
        }

        auto sleOffer = std::make_shared<SLE>(ltOFFER, offer_index);
        sleOffer->setAccountID (sfAccount, account_);
        sleOffer->setFieldU32 (sfSequence, uSequence);
        sleOffer->setFieldH256 (sfBookDirectory, dir.key);
        sleOffer->setFieldAmount (sfTakerPays, saTakerPays);
        sleOffer->setFieldAmount (sfTakerGets, saTakerGets);
        sleOffer->setFieldU64 (sfOwnerNode, *ownerNode);
        sleOffer->setFieldU64 (sfBookNode, *bookNode);
        if (expiration)
            sleOffer->setFieldU32 (sfExpiration, *expiration);
        if (bPassive)
            sleOffer->setFlag (lsfPassive);
        if (bSell)
            sleOffer->setFlag (lsfSell);
        sb.insert(sleOffer);

        if (!bookExisted)
            ctx_.app.getOrderBookDB().addOrderBook(book);

        JLOG (j_.debug()) << "final result: success";

        return { tesSUCCESS, true };
    }

}
