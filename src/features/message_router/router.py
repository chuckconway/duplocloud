from src.intents.ask_llm_intent import AskLLMIntent
from src.intents.error_intent import ErrorAction
from src.intents.new_conversation import NewConversation


def get_action(action_name: str) -> lambda emit, data: None:
    new_action = lambda emit, message, session: ErrorAction(emit=emit, message=message, session=session)

    for action in action_list():
        if action[0] == action_name:
            new_action = action[1]



    return new_action


def action_list() -> list[(str, lambda emit: None)]:
    return [
        (NewConversation.action_name, lambda emit, message, session: NewConversation(emit=emit, message=message, session=session)),
        (AskLLMIntent.action_name, lambda emit, message, session: AskLLMIntent(emit=emit, message=message, session=session)),

        # (ParseCustomer.action_name, lambda emit, message, session: ParseCustomer(emit=emit, message=message, session=session)),
        # (DiscountCode.action_name, lambda emit, message, session: DiscountCode(emit=emit, message=message, session=session)),
        # (ConfirmCustomer.action_name, lambda emit, message, session: ConfirmCustomer(emit=emit, message=message, session=session)),
        # (ProductList.action_name, lambda emit, message, session: ProductList(emit=emit, message=message, session=session)),
        # (ProductConfirmation.action_name, lambda emit, message, session: ProductConfirmation(emit=emit, message=message, session=session)),
    ]