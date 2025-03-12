import { v4 as uuidv4 } from 'uuid';

export function getOrCreateUUID(): string {
    const localStorageKey: string = "UUID";

    // Check if UUID exists in localStorage
    let uuid = localStorage.getItem(localStorageKey);

    // If UUID does not exist, create a new one
    if (!uuid) {
        uuid = generateUUID();
        localStorage.setItem(localStorageKey, uuid);
    }

    return uuid;
}

function generateUUID(): string {
    return uuidv4();
}