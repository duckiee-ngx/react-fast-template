import { z } from "zod";

const envSchema = z.object({
  VITE_API_URL: z.url(),
});

const parsed = envSchema.safeParse(import.meta.env);

if (!parsed.success) {
  console.error("Invalid environment variables:", z.prettifyError(parsed.error));
  throw new Error("Invalid environment variables. Check .env against .env.example");
}

export const env = parsed.data;
