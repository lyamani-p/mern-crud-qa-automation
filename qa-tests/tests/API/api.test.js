const request = require('supertest');
const app = require('C:/Users/aboly/Downloads/crud_project_with_tests/mern-crud-auth-master/src/app.js');

const EMAIL = "lyama@gmail.com";
const PASSWORD = "123456789";

describe("Full task CRUD flow", () => {
    let token;
    let taskId;

    test("Register test user (ignore if exists)", async () => {
        const res = await request(app)
            .post('/api/auth/register')
            .send({ email: EMAIL, password: PASSWORD, name: "Test User" });
        expect([200, 201, 400, 409]).toContain(res.statusCode);
    });

    test("Login and get token", async () => {
        const res = await request(app)
            .post('/api/auth/login')
            .send({ email: EMAIL, password: PASSWORD });
        expect(res.statusCode).toBe(200);
        // Assuming token is returned in cookie
        const cookies = res.headers['set-cookie'];
        expect(cookies).toBeDefined();
        // Extract token from cookie (adjust according to your cookie name)
        const tokenCookie = cookies.find(cookie => cookie.startsWith('token='));
        expect(tokenCookie).toBeDefined();
        token = tokenCookie.split(';')[0].split('=')[1];
        expect(token).toBeTruthy();
    });

    test("Create a task", async () => {
        const res = await request(app)
            .post('/api/tasks')
            .set('Cookie', `token=${token}`)
            .send({
                title: "LYAMANI API Task",
                description: "Created by LYAMANI",
                date: "2025-07-24T00:00:00.000Z"
            });
        expect([200, 201]).toContain(res.statusCode);
        taskId = res.body._id;
        expect(taskId).toBeDefined();
    });

    test("Get tasks", async () => {
        const res = await request(app)
            .get('/api/tasks')
            .set('Cookie', `token=${token}`);
        expect(res.statusCode).toBe(200);
        expect(Array.isArray(res.body)).toBe(true);
    });

    test("Update task", async () => {
        const res = await request(app)
            .put(`/api/tasks/${taskId}`)
            .set('Cookie', `token=${token}`)
            .send({ title: "Updated Title" });
        expect(res.statusCode).toBe(200);
        expect(res.body.title).toBe("Updated Title");
    });

    test("Delete task", async () => {
        const res = await request(app)
            .delete(`/api/tasks/${taskId}`)
            .set('Cookie', `token=${token}`);
        expect(res.statusCode).toBe(204);
    });
});
