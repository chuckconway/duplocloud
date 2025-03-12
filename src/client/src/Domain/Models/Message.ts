export interface IMessage {
    actionName: string;
    purpose?: string;
    message: string;
    options?: string[];
    sender: string;
    uuid: string | null;
}

export class Message implements IMessage {

    constructor(public message: string,
                public options: string[],
                public purpose: string,
                public sender: string,
                public uuid: string | null = null,
                public actionName: string = "") {

    }

}