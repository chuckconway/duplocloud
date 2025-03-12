import React, {useEffect, useRef} from "react";
import "./Conversation.css";
import {ConversationProps} from "../../Domain/Models/ConversationProps";
import Markdown from "react-markdown";

const Conversation: React.FC<ConversationProps> = props => {
    // const [messages, setMessages] = useState<IMessage[]>([]);
    const dummyRef = useRef<HTMLDivElement>(null);
    const bodyRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (dummyRef && dummyRef.current && bodyRef && bodyRef.current) {
            bodyRef.current.scrollTo({
                top: dummyRef.current.offsetTop,
                behavior: "smooth"
            });
        }
    }, [props.newMessages]);

    // @ts-ignore
    return (
        <div className="message-container" ref={bodyRef}>
            {props.newMessages.map(chat => (
                <div key={chat.message}>
                    {chat.sender === "bot" ? <strong>Benny</strong>: <strong style={{textAlign:"right", marginRight:"10px"}}>You</strong>}
                    <div className={`message ${chat.sender}`}>
                        <Markdown>{chat.message}</Markdown>
                    </div>
                    {chat.options ? (
                        <div className="options">
                            <div>
                                <i className="far fa-hand-pointer"></i>
                            </div>

                            {chat.options.map((option: any) => (
                                <p
                                    onClick={e => props.optionClick(e)}
                                    data-id={option}
                                    key={option}
                                >
                                    {option}
                                </p>
                            ))}
                        </div>
                    ) : null}
                    <div ref={dummyRef} className="dummy-div"></div>
                </div>
            ))}
        </div>
    );
};

export default Conversation;