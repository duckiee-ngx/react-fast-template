import { useEffect, useRef } from "react"

export function useClickOutside(callback?: () => void) {
  const nodeRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    function handleClickOutSide(this: Document, ev: MouseEvent) {
      if (nodeRef.current && !nodeRef.current.contains(ev.target as Node)) {
        callback?.()
      }
    }

    document.addEventListener("mouseup", handleClickOutSide)

    return () => {
      document.removeEventListener("mouseup", handleClickOutSide)
    }
  }, [callback])

  return {
    nodeRef,
  }
}
