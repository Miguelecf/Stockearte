// src/components/NotFound.tsx
import React from "react";
import styled from "styled-components";

const NotFound: React.FC = () => {
  return (
    <Container>
      <h1>404</h1>
      <p>Page not found!</p>
    </Container>
  );
};

export default NotFound;

const Container = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  flex-direction: column;
  background-color: #ffebee;

  h1 {
    font-size: 4rem;
    color: #d32f2f;
  }

  p {
    font-size: 1.5rem;
    color: #b71c1c;
  }
`;
