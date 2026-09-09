import { registerSessionNavigator } from "@src/modules/auth/utils/session";
import {
  createRouter,
  RouterProvider as TanstackRouterProvider,
} from "@tanstack/react-router";
import { routeTree } from "../routeTree.gen";
import { queryClient } from "./query-provider";

const router = createRouter({
  routeTree,
  context: { queryClient },
});

registerSessionNavigator(() => {
  void router.navigate({ to: "/login", replace: true });
});

// Register the router instance for type safety
declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router;
  }
}

const RouterProvider = () => {
  return <TanstackRouterProvider router={router} />;
};

export default RouterProvider;
