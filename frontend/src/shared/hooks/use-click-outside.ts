import { useEffect, useRef } from "react";

export function useClickOutside<T extends HTMLElement = HTMLElement>(
  callback?: () => void,
) {
  const nodeRef = useRef<T>(null);
  const callbackRef = useRef(callback);
  callbackRef.current = callback;

  useEffect(() => {
    function handlePointerDown(event: PointerEvent) {
      if (event.pointerType === "mouse" && event.button !== 0) return;

      const node = nodeRef.current;
      const target = event.target;
      if (node && target instanceof Node && !node.contains(target)) {
        callbackRef.current?.();
      }
    }

    document.addEventListener("pointerdown", handlePointerDown);

    return () => {
      document.removeEventListener("pointerdown", handlePointerDown);
    };
  }, []);

  return { nodeRef };
}
