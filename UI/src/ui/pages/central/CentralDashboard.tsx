import { Link } from "react-router-dom";
import { styled } from "styled-components";

const CentralDashboard = () => {
  return (
    <DashboardContainer>
      <DashboardTitle>Dashboard Casa Central</DashboardTitle>
      <DashboardNavigation>
        <NavItem>
          <StyledLink to="/central-dashboard/stores">Gestión de Tiendas</StyledLink>
        </NavItem>
        <NavItem>
          <StyledLink to="/central-dashboard/users">Gestión de Usuarios</StyledLink>
        </NavItem>
        <NavItem>
          <StyledLink to="/central-dashboard/products">Gestión de Productos</StyledLink>
        </NavItem>
      </DashboardNavigation>
    </DashboardContainer>
  );
};

const DashboardContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #f2f2f2;
`;

const DashboardTitle = styled.h1`
  font-size: 3rem;
  margin-bottom: 3rem;
  color: #333;
`;

const DashboardNavigation = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const NavItem = styled.div`
  padding: 1rem 2rem;
  background-color: #fff;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const StyledLink = styled(Link)`
  text-decoration: none;
  color: #333;
  font-weight: bold;
`;

export default CentralDashboard;