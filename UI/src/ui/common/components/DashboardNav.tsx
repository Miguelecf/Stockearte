import { Link } from "react-router-dom";
import { styled } from "styled-components";

const DashboardNav = () => {
  return (
    <NavContainer>
      <ul>
        <li>
          <Link to="/central-dashboard/stores">Gestión de Tiendas</Link>
        </li>
        <li>
          <Link to="/central-dashboard/users">Gestión de Usuarios</Link>
        </li>
        <li>
          <Link to="/central-dashboard/products">Gestión de Productos</Link>
        </li>
      </ul>
    </NavContainer>
  );
};

const NavContainer = styled.nav`
  margin: 20px 0;

  ul {
    list-style-type: none;
    padding: 0;

    li {
      margin: 10px 0;
    }
  }

  a {
    text-decoration: none;
    color: #00796b;
    font-weight: bold;

    &:hover {
      text-decoration: underline;
    }
  }
`;

export default DashboardNav;
