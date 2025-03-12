import React from "react";
import {IMessage} from "./Message";


export interface ConversationProps {
    newMessages: IMessage[];
    optionClick: (ev: React.MouseEvent<HTMLElement>) => void;
}