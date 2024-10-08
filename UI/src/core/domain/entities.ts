export interface Store {
  code: string;
  address: string;
  city: string;
  state: string;
  enabled: boolean;
}

export interface Product {
  name: string;
  uniqueCode: string;
  size: string;
  imageUrl: string;
  color: string;
  enabled: boolean;
}

export interface User {
  username: string;
  password: string;
  firstName: string;
  lastName: string;
  enabled: boolean;
  isCentral: boolean;
}
