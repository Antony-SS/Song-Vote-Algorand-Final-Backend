import os
from pyteal import *

def approval_program():
    handle_creation = Seq(
        App.globalPut(Bytes("Count1"), Int(0)),
        App.globalPut(Bytes("Count2"), Int(1)),
        Return(Int(1))
    )

    handle_optin = Return(Int(0))

    handle_closeout = Return(Int(0))

    handle_updateapp = Return(Int(0))

    handle_deleteapp = Return(Int(0))

    scratchCount = ScratchVar(TealType.uint64)


    addC1 = Seq(
        scratchCount.store(App.globalGet(Bytes("Count1"))), 
        App.globalPut(Bytes("Count1"), scratchCount.load() + Int(1)),
        Return(Int(1))
    )

    addC2 = Seq(
        scratchCount.store(App.globalGet(Bytes("Count2"))), 
        App.globalPut(Bytes("Count2"), scratchCount.load() + Int(1)),
        Return(Int(1))
    )

    handle_noop = Seq(
        # First, fails immediately if this transaction is grouped with others
        Assert(Global.group_size() == Int(1)), 
        Cond(
            [Txn.application_args[0] == Bytes("AddC1"), addC1], 
            [Txn.application_args[0] == Bytes("AddC2"), addC2]
        )
    )

    program = Cond(
        [Txn.application_id() == Int(0), handle_creation],
        [Txn.on_completion() == OnComplete.OptIn, handle_optin],
        [Txn.on_completion() == OnComplete.CloseOut, handle_closeout],
        [Txn.on_completion() == OnComplete.UpdateApplication, handle_updateapp],
        [Txn.on_completion() == OnComplete.DeleteApplication, handle_deleteapp],
        [Txn.on_completion() == OnComplete.NoOp, handle_noop]
    )
    return compileTeal(program, Mode.Application, version=5)

def clear_state_program():
    program = Return(Int(1))
    # Mode.Application specifies that this is a smart contract
    return compileTeal(program, Mode.Application, version=5)

if __name__ == "__main__":

    path = "./contracts/artifacts"
    
    with open(os.path.join(path, "songvote_approval.teal"), 'w') as f:
        f.write(approval_program())
    
    with open(os.path.join(path, "songvote_clear.teal"), 'w') as f:
        f.write(clear_state_program())
    

