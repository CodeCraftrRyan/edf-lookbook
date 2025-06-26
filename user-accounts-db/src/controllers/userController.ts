class UserController {
    constructor(private userModel: any) {}

    async createUser(req: any, res: any) {
        try {
            const userData = req.body;
            const newUser = await this.userModel.create(userData);
            res.status(201).json(newUser);
        } catch (error) {
            res.status(500).json({ message: 'Error creating user', error });
        }
    }

    async getUser(req: any, res: any) {
        try {
            const userId = req.params.id;
            const user = await this.userModel.findById(userId);
            if (user) {
                res.status(200).json(user);
            } else {
                res.status(404).json({ message: 'User not found' });
            }
        } catch (error) {
            res.status(500).json({ message: 'Error retrieving user', error });
        }
    }

    async updateUser(req: any, res: any) {
        try {
            const userId = req.params.id;
            const updatedData = req.body;
            const updatedUser = await this.userModel.update(userId, updatedData);
            if (updatedUser) {
                res.status(200).json(updatedUser);
            } else {
                res.status(404).json({ message: 'User not found' });
            }
        } catch (error) {
            res.status(500).json({ message: 'Error updating user', error });
        }
    }

    async deleteUser(req: any, res: any) {
        try {
            const userId = req.params.id;
            const deletedUser = await this.userModel.delete(userId);
            if (deletedUser) {
                res.status(204).send();
            } else {
                res.status(404).json({ message: 'User not found' });
            }
        } catch (error) {
            res.status(500).json({ message: 'Error deleting user', error });
        }
    }
}

export default UserController;