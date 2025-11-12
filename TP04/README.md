# TP04 — Dockerized TP03 (with PBIX inside the image)

يحتوي هذا المشروع على:
- كود TP03 الحقيقي، البيانات المنظفة، والصور.
- ملف Power BI (.pbix) مضمَّن داخل الصورة في `/app/report`.
- خادم Flask على المنفذ 80 لعرض وتنزيل المخرجات.

## الأوامر السريعة
```bash
docker login
bash scripts/build_push.sh     # عدّل DOCKER_USERNAME/IMAGE_NAME/TAG أولاً
bash scripts/run_three.sh      # يشغّل 3 حاويات ويربط 8081/8082/8083 → 80
docker ps
# تصفح:
#   http://localhost:8081
#   http://localhost:8082
#   http://localhost:8083
```

## الملفات المهمة
- `Dockerfile`, `requirements.txt`, `app.py`
- `TP03_analysis.py`
- `TP03_sales_data.csv`, `TP03_sales_data_clean.csv`, `customer_segments.csv`
- `figures/` (sales_over_time.png, top_products.png, revenue_by_region.png, customer_segments.png)
- `report/PowerBI_Sales_Dashboard.pbix`
- `scripts/*.sh`, `docker-compose.yml`
