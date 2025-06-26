import { Router } from 'express';
import { UserController } from '../controllers/userController';

const router = Router();
const userController = new UserController();

export function setUserRoutes(app) {
    app.use('/api/users', router);

    router.post('/', userController.createUser.bind(userController));
    router.get('/:id', userController.getUser.bind(userController));
    router.put('/:id', userController.updateUser.bind(userController));
    router.delete('/:id', userController.deleteUser.bind(userController));
}