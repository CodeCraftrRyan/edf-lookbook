import { Sequelize, DataTypes, Model } from 'sequelize';

// Database connection setup
const sequelizeInstance = new Sequelize('database', 'username', 'password', {
    host: 'localhost',
    dialect: 'mysql',
});

export const sequelize = sequelizeInstance;
export default sequelizeInstance;

export class User extends Model {
    public id!: number;
    public username!: string;
    public password!: string;
    public email!: string;
}

User.init(
    {
        id: {
            type: DataTypes.INTEGER,
            autoIncrement: true,
            primaryKey: true,
        },
        username: {
            type: DataTypes.STRING,
            allowNull: false,
            unique: true,
        },
        password: {
            type: DataTypes.STRING,
            allowNull: false,
        },
        email: {
            type: DataTypes.STRING,
            allowNull: false,
            unique: true,
        },
    },
    {
        sequelize: sequelizeInstance,
        modelName: 'User',
        tableName: 'users',
        timestamps: true,
    }
);