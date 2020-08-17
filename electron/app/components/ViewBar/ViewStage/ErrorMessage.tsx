import React, { useEffect, useRef, useState } from "react";
import { animated, useSpring } from "react-spring";
import styled from "styled-components";
import { useService } from "@xstate/react";

import { useOutsideClick } from "../../../utils/hooks";

const ErrorMessageDiv = animated(styled.div`
  box-sizing: border-box;
  border: 2px solid ${({ theme }) => theme.error};
  background-color: ${({ theme }) => theme.backgroundDark};
  color: ${({ theme }) => theme.fontDark};
  border-radius: 2px;
  padding: 0.5rem;
  line-height: 1rem;
  margin-top: 2.5rem;
  font-weight: bold;
  box-shadow: 0 2px 20px ${({ theme }) => theme.backgroundDark};
  position: fixed;
  width: auto;
  z-index: 800;
`);

const ErrorMessage = React.memo(({ serviceRef, style }) => {
  const [state, send] = useService(serviceRef);
  const ref = useRef();
  const [errorTimeout, setErrorTimeout] = useState(null);
  const { error, errorId } = state.context;
  const animations = useSpring({
    opacity: errorId ? 1 : 0,
    from: {
      opacity: 0,
    },
  });

  useEffect(() => {
    errorTimeout && clearTimeout(errorTimeout);
    !errorId && setErrorTimeout(setTimeout(() => send("CLEAR_ERROR"), 1000));
  }, [errorId]);

  useOutsideClick(ref, () => send("CLEAR_ERROR_ID"));

  return (
    <ErrorMessageDiv
      ref={ref}
      style={{ ...animations, display: error ? "block" : "none", ...style }}
    >
      {error}
    </ErrorMessageDiv>
  );
});

export default ErrorMessage;
