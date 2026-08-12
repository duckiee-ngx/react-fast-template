import { z } from "zod";

export type TokenResponse = {
  accessToken: string;
  refreshToken?: string;
};

export const loginRequestSchema = z.object({
  email: z.email(),
  password: z.string().min(8),
});

export type LoginRequest = z.infer<typeof loginRequestSchema>;
