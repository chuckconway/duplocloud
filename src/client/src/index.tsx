import React from 'react';
import { createRoot } from 'react-dom/client';
import "./index.css";
import "./App.css";

import App from "./App";
const container = document.getElementById('app');

if(!container) {
    throw new Error("Could not find #app element");
}

const root = createRoot(container); // createRoot(container!) if you use TypeScript
root.render(<App />);