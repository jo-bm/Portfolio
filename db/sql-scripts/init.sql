CREATE TABLE parties (
  id INT AUTO_INCREMENT PRIMARY KEY,
  party_name VARCHAR(255),
  platform TEXT
);

CREATE TABLE tbl_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    vote_entitlement VARCHAR(255) NOT NULL,
    voted VARCHAR(255) NOT NULL
);

CREATE TABLE parties_statistic (
  id INT AUTO_INCREMENT PRIMARY KEY,
  party_name VARCHAR(255),
  votes_number INT DEFAULT 0
);


INSERT INTO tbl_user (user_id, vote_entitlement, voted) VALUES 
('964501563', 'true', 'false'),
('177876653', 'true', 'false'),
('035686674', 'true', 'false'),
('672477031', 'false', 'false'),
('413743345', 'true', 'false'),
('093175180', 'true', 'false'),
('468389937', 'false', 'false'),
('087926721', 'true', 'false'),
('298250838', 'true', 'false'),
('328664701', 'true', 'false'),
('798332409', 'false', 'false'),
('398759266', 'false', 'false'),
('601638695', 'true', 'false'),
('681278263', 'true', 'false'),
('510684194', 'true', 'false'),
('979533981', 'false', 'false'),
('640309290', 'true', 'false'),
('432901288', 'true', 'false'),
('855708863', 'true', 'false'),
('301398160', 'false', 'false');

















