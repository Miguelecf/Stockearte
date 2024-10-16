import { Link } from "react-router-dom";
import { styled } from "styled-components";

const CentralDashboard = () => {
  const isCentral = JSON.parse(localStorage.getItem("isCentral") as string);

  return (
    <Container>
      <h1>Dashboard Casa Central</h1>
      <nav>
        <ul>
          {isCentral && (
            <>
              <li>
                <Link to="/central-dashboard/stores">Gestión de Tiendas</Link>
              </li>
              <li>
                <Link to="/central-dashboard/users">Gestión de Usuarios</Link>
              </li>
            </>
          )}
          <li>
            <Link to="/">Logout</Link>
          </li>

          <li>
            <Link to="/central-dashboard/products">Gestión de Productos</Link>
          </li>
        </ul>
      </nav>
    </Container>
  );
};

const Container = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #e0f7fa;
  h1 {
    font-size: 3rem;
    color: #00796b;
  }
  p {
    font-size: 1.5rem;
    color: #004d40;
  }
`;

export default CentralDashboard;
