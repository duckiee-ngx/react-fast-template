import QueryProvider from "./providers/query-provider";
import RouterProvider from "./providers/router-provider";

const App = () => {
  return (
    <QueryProvider>
      <RouterProvider />
    </QueryProvider>
  );
};

export default App;
