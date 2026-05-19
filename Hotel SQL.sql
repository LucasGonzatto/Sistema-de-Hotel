USE hotel;

DROP TABLE IF EXISTS clientes;

CREATE TABLE clientes (

    id INT AUTO_INCREMENT PRIMARY KEY,

    descricao VARCHAR(255) NOT NULL,

    status ENUM(
        'ocupado',
        'livre',
        'reservado'
    ) NOT NULL,

    check_in DATE NOT NULL,

    check_out DATE NOT NULL,

    quarto INT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);