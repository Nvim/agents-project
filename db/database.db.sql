DROP TABLE IF EXISTS clients;
DROP TABLE IF EXISTS produits;

CREATE TABLE clients (
    id_client VARCHAR(10) PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    email VARCHAR(150),
    ville VARCHAR(100),
    solde_compte DECIMAL(12,2) DEFAULT 0,
    type_compte VARCHAR(20) NOT NULL,
    date_inscription DATE,
    achats_total DECIMAL(12,2) DEFAULT 0
);

CREATE TABLE produits (
    id_produit VARCHAR(10) PRIMARY KEY,
    nom VARCHAR(150) NOT NULL,
    prix_ht DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0
);

INSERT INTO clients (
    id_client, nom, email, ville, solde_compte, type_compte, date_inscription, achats_total
) VALUES
('C001', 'Marie Dupont', 'marie.dupont@email.fr', 'Paris', 15420.50, 'Premium', '2021-03-15', 8750.00),
('C002', 'Jean Martin', NULL, NULL, 3200.00, 'Standard', NULL, 0),
('C003', 'Sophie Bernard', NULL, NULL, 28900.00, 'VIP', NULL, 0),
('C004', 'Lucas Petit', NULL, NULL, 750.00, 'Standard', NULL, 0);

INSERT INTO produits (
    id_produit, nom, prix_ht, stock
) VALUES
('P001', 'Ordinateur portable Pro', 899.00, 45),
('P002', 'Souris ergonomique', 49.90, 120),
('P003', 'Bureau réglable', 350.00, 18),
('P004', 'Casque audio sans fil', 129.00, 67),
('P005', 'Écran 27 pouces 4K', 549.00, 30);
