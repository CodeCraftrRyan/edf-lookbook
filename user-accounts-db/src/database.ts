import { Sequelize } from 'sequelize';

const db = new Sequelize('user_accounts', 'username', 'password', {
    host: 'localhost',
    dialect: 'sqlite',
    logging: false,
});

const initializeDatabase = async () => {
    try {
        await db.authenticate();
        console.log('Connection has been established successfully.');
        
        // Define the User model here if needed
        // await db.sync(); // Uncomment to create tables if they don't exist
    } catch (error) {
        console.error('Unable to connect to the database:', error);
    }
};

export const connectDatabase = initializeDatabase;
export const database = db;
