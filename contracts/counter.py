from pyteal import *

def approval_program():
    handle_creation = Seq(
        App.globalPut(Bytes("Count"), Int(0)),
        Return(Int(1))
    )

    handle_optin = Return(Int(0))

    handle_closeout = Return(Int(0))

    handle_updateapp = Return(Int(0))

    handle_deleteapp = Return(Int(0))

    scratchCount = ScratchVar(TealType.uint64)

    add = Seq(
        # The initial `store` for the scratch var sets the value to 
        # whatever is in the `Count` global state variable
        scratchCount.store(App.globalGet(Bytes("Count"))), 
        # Increment the value stored in the scratch var 
        # and update the global state variable 
        App.globalPut(Bytes("Count"), scratchCount.load() + Int(1)),
        Return(Int(1))
    )

    deduct = Seq(
        # The initial `store` for the scratch var sets the value to 
        # whatever is in the `Count` global state variable
        scratchCount.store(App.globalGet(Bytes("Count"))),
        # Check if the value would be negative by decrementing 
        If(scratchCount.load() > Int(0),
            # If the value is > 0, decrement the value stored 
            # in the scratch var and update the global state variable
            App.globalPut(Bytes("Count"), scratchCount.load() - Int(1)),
        ),
        Return(Int(1))
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

print(approval_program())