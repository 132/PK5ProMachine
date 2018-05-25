//
// Created by bialan132 on 5/9/18.
//

#ifndef RIPPLE_TX_LOGTRANSACTION_H
#define RIPPLE_TX_LOGTRANSACTION_H

#include <ripple/app/tx/impl/Transactor.h>
#include <ripple/basics/Log.h>
#include <ripple/protocol/TxFlags.h>
#include <ripple/protocol/types.h>

#include <ripple/app/tx/impl/OfferStream.h>
#include <ripple/app/tx/impl/Taker.h>
#include <ripple/app/tx/impl/Transactor.h>
#include <utility>

namespace ripple {

    class LogTransaction
            : public Transactor {

    public:

        LogTransaction (ApplyContext& ctx)
                : Transactor(ctx){
        }

        static
        TER
        preflight (PreflightContext const& ctx);

        static
        TER
        preclaim(PreclaimContext const& ctx);

        void
        preCompute() override;

        TER
        doApply() override;
    };

}
#endif //RIPPLED_LOGTRANSACTION_H
