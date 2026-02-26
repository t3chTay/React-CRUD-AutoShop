# React + Vite

## Live Testing

**Backend (Render):** https://react-crud-autoshop.onrender.com  
**Swagger Docs:** https://react-crud-autoshop.onrender.com/docs  

## How to Test (Quick)

1. Open Swagger docs: https://react-crud-autoshop.onrender.com/docs
2. Register a mechanic using `POST /mechanics/`
3. Login using `POST /mechanics/login` to get a token
4. Click **Authorize** and paste: `Bearer <token>`
5. Test protected routes (update/delete/my-tickets)

## Run Tests

```bash
python -m unittest discover -s tests -p "test*.py"
```
------

If you also deploy the frontend, add:

```md
**Frontend (Render):** https://YOUR-FRONTEND.onrender.com