import { type Dispatch, type SetStateAction, useEffect, useState } from "react"

type UseDebounce<T> = [T, Dispatch<SetStateAction<T>>, T]
type InitialValue<T> = T | (() => T)

export function useDebounce<T>(initialValue: InitialValue<T>, delay = 500): UseDebounce<T> {
  const [value, setValue] = useState<T>(initialValue)
  const [debounceValue, setDebounceValue] = useState<T>(initialValue)

  useEffect(() => {
    const handler = setTimeout(() => setDebounceValue(value), delay)
    return () => clearTimeout(handler)
  }, [value, delay])

  return [value, setValue, debounceValue]
}
