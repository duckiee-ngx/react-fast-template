import { ensureSession } from "@src/modules/auth/utils/session";
import { createFileRoute, Outlet, redirect } from "@tanstack/react-router";

export const Route = createFileRoute("/_protected")({
  beforeLoad: async () => {
    const isSessionValid = await ensureSession();
    if (!isSessionValid) {
      throw redirect({ to: "/login" });
    }
  },
  component: () => <Outlet />,
});
