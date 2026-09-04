import type { FileRoutesByFullPath } from "@src/routeTree.gen";
import { type ReactNode, useEffect, useState } from "react";
import { useRefreshTokenMutation } from "../query";

const UNAUTHORIZED_PATHS: (keyof FileRoutesByFullPath)[] = ["/auth/login"];

export default function AuthProvider({ children }: { children: ReactNode }) {
  const [bootstrapped, setBootstrapped] = useState(false);
  const { mutate: refreshTokenMutate } = useRefreshTokenMutation();

  useEffect(() => {
    if (
      UNAUTHORIZED_PATHS.includes(
        window.location.pathname as keyof FileRoutesByFullPath,
      )
    ) {
      setBootstrapped(true);
      return;
    }

    refreshTokenMutate(undefined, { onSuccess: () => setBootstrapped(true) });
  }, [refreshTokenMutate]);

  if (!bootstrapped) {
    return <div>Loading...</div>;
  }

  return children;
}
