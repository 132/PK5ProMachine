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

/*        if (ctx.tx.getFlags() & tfUniversalMask)
        {
            // There are no flags (other than universal) for CreateCheck yet.
            JLOG(ctx.j.warn()) << "Malformed transaction: Invalid flags set.";
            return temINVALID_FLAG;
        }*/
/*        if (ctx.tx[sfAccount] == ctx.tx[sfDestination])
        {
            // They wrote a check to themselves.
            JLOG(ctx.j.warn()) << "Malformed transaction: Check to self.";
            return temREDUNDANT;
        }*/

/*        if (auto const optExpiry = ctx.tx[~sfExpiration])
        {
            if (*optExpiry == 0)
            {
                JLOG(ctx.j.warn()) << "Malformed transaction: bad expiration";
                return temBAD_EXPIRATION;
            }
        }*/

        std::cout<<"Go to logTransaction.cpp before call preflight2" << std::endl;
        return preflight2 (ctx);
    }


    TER
    LogTransaction::preclaim (PreclaimContext const& ctx)
    {
        std::cout<<"Go to  LogTransaction::preclaim in logTransaction.cpp" << std::endl;

        auto const id = ctx.tx[sfAccount];

        std::cout<<"Go to  LogTransaction::preclaim before uTxFlags " << std::endl;
        std::uint32_t const uTxFlags = ctx.tx.getFlags();

        std::cout<<"Go to  LogTransaction::preclaim before sle " << std::endl;
        auto const sle = ctx.view.read(keylet::account(id));

        std::cout<<"Go to  LogTransaction::preclaim before uFlagsIn " << std::endl;
        std::uint32_t const uFlagsIn = sle->getFieldU32(sfFlags);

///////////////// problem from here -------------
/*Cmt to run
        std::cout<<"Go to  LogTransaction::preclaim before uSetFlag " << std::endl;
        std::uint32_t const uSetFlag = ctx.tx.getFieldU32(sfSetFlag);

        std::cout<<"Go to  LogTransaction::preclaim before bSetRequireAuth " << std::endl;
        // legacy AccountSet flags
        bool bSetRequireAuth = (uTxFlags & tfRequireAuth) || (uSetFlag == asfRequireAuth);

        //
        // RequireAuth
        //
        std::cout<<"Go to  LogTransaction::preclaim before checking to get the problem" << std::endl;
        if (bSetRequireAuth && !(uFlagsIn & lsfRequireAuth))
        {
            if (!dirIsEmpty(ctx.view,
                            keylet::ownerDir(id)))
            {
                std::cout<<"Go to  LogTransaction::preclaim in problem with authen" << std::endl;
                JLOG(ctx.j.trace()) << "Retry: Owner directory not empty.";
                return (ctx.flags & tapRETRY) ? terOWNERS : tecOWNERS;
            }
        }*/

        std::cout<<"Go to  LogTransaction::preclaim after checking and return tesSUCCESS" << std::endl;
        return tesSUCCESS;
    }

    TER
    LogTransaction::doApply ()
    {

        return tesSUCCESS;
    }

    void LogTransaction::preCompute(){

    }

    LogTransaction::LogTransaction (ApplyContext& ctx)
    : Transactor(ctx){
    }

}
