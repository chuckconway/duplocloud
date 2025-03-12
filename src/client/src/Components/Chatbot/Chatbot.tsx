import React, {useEffect, useState} from "react";

import "./Chatbot.css";

import io from 'socket.io-client';

import Conversation from "../Conversation/Conversation";
import {getOrCreateUUID} from "../../Domain/Services/User";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import { faPaperPlane } from '@fortawesome/free-solid-svg-icons'
import {Message, IMessage} from "../../Domain/Models/Message";

const socket = io('http://127.0.0.1:5000');

function arrayBufferToObject(buffer: ArrayBuffer): any {
    // Step 1: Convert ArrayBuffer to string
    const decoder = new TextDecoder('utf-8');
    const jsonString = decoder.decode(buffer);

    // Step 2: Parse the JSON string to an object
    try {
        return JSON.parse(jsonString);
    } catch (e) {
        console.error("Error parsing JSON", e);
        return null;
    }
}

function sendMessage(message: IMessage) {
    socket.emit('message', message);
}

function getBlankResponseBotMessage() {
    const chatbotResponses: string[] = [
        "Ah, the classic invisible ink! Let me put on my special glasses... Nope, still can't see anything. Your secret message is safe with me!",
        "Processing your message... Error 404: Words not found. Please reboot your keyboard and try again.",
        "Ah, a silent treatment, eh? Well, two can play at that game... 🤫 ...Okay, I give up, you win!",
        "Looks like your message took a detour through the Bermuda Triangle. Don't worry, I'll send out a search party for those missing words!",
        "Playing hide and seek with your words, huh? Challenge accepted – I still haven't found them!"
    ];

        const randomIndex = Math.floor(Math.random() * chatbotResponses.length);
        return new Message(chatbotResponses[randomIndex], [], "", "bot", "");
}

const Chatbot: React.FC = () => {
    const [userKeyStrokes, setUserKeyStrokes] = useState<string>("");
    const [newMessages, setNewMessages] = useState<IMessage[]>([]);

    const [userMessage, setUserMessage] = useState<IMessage | null>(null);
    const [botMessage, setBotMessage] = useState<IMessage | null>(null);
    const [currentAction, setCurrentAction] = useState<string>("");

    useEffect(() => {
        sendMessage(new Message("Hello", [], "", "user", getOrCreateUUID(), "new_conversation"));

        socket.on('message', (reply: ArrayBuffer) => {
            const message = arrayBufferToObject(reply);
            setCurrentAction(message.action_name);

            setBotMessage(message);
        });
    }, []);

    useEffect(() => {
        if (!userMessage) {
            return;
        }
        addMessage(userMessage);
        setUserMessage(null);
    }, [userMessage]);


    useEffect(() => {
        if (!botMessage) {
            return;
        }

        addMessage(botMessage);
        setBotMessage(null);

    }, [botMessage]);

     const addMessage = (message: IMessage) => {
        let tempArray = [...newMessages];

        tempArray.push(message);
        setNewMessages(tempArray);
    };

    const optionClick = (e: React.MouseEvent<HTMLElement>) => {
        let option = e.currentTarget.dataset.id;
        if (option) {
            // setNextStep(option);
        }
    };

    // event handlers
    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setUserKeyStrokes(e.target.value);
    };

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        if (!userKeyStrokes) {
            const errorMessage = getBlankResponseBotMessage();
            setBotMessage(errorMessage);
            return;
        }

        const uuid = getOrCreateUUID();

        const message = new Message(userKeyStrokes,[], "", "user", uuid, currentAction );
        console.log(message);
        setUserMessage(message);
        sendMessage(message);

        setUserKeyStrokes("")
    };

    return (
        <div className="chat-container">
            <Conversation
                newMessages={newMessages}
                optionClick={optionClick}
            />
            <form onSubmit={e => handleSubmit(e)} className="form-container">
                <input
                    onChange={e => handleInputChange(e)}
                    value={userKeyStrokes}
                ></input>
                <button>
                    <FontAwesomeIcon icon={faPaperPlane} />
                </button>
            </form>
        </div>
    );
};

export default Chatbot;