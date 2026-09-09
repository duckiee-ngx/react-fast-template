import "./configs/env";
import "./index.css";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import { attachAuthInterceptors } from "./modules/auth/http-interceptors";
import { httpClient } from "./shared/api/http-client";

const root = document.getElementById("root")!;

attachAuthInterceptors(httpClient);

createRoot(root).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
