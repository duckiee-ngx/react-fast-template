import AuthProvider from "./modules/auth/providers/auth-provider"
import QueryProvider from "./providers/query-provider"
import RouterProvider from "./providers/router-provider"

const App = () => {
  return (
    <QueryProvider>
      <AuthProvider>
        <RouterProvider />
      </AuthProvider>
    </QueryProvider>
  )
}

export default App
