# MongoDB TP -- خطوات كاملة + الأوامر

## 1. تشغيل MongoDB

### تشغيل السيرفر (mongod)

``` bat
cd C:\MongoDB\bin
mongod.exe
```

> يتم تخزين البيانات تلقائيًا في `C:\data\db` لأن MongoDB 2.6 يستعمل هذا
> المسار كمسار افتراضي.

------------------------------------------------------------------------

## 2. تشغيل Mongo Shell

``` bat
cd C:\MongoDB\bin
mongo.exe
```

------------------------------------------------------------------------

## 3. اختيار قاعدة البيانات

``` js
use info
db
```

------------------------------------------------------------------------

## 4. إدخال البيانات (Insert)

MongoDB 2.6 يستعمل:

``` js
insert()
```

### المنتج 1

``` js
db.produits.insert({
  nom: "Macbook Pro",
  fabriquant: "Apple",
  prix: 11435.99,
  options: [
    "Intel Core i5",
    "Retina Display",
    "Long life battery"
  ]
})
```

### المنتج 2

``` js
db.produits.insert({
  nom: "Macbook Air",
  fabriquant: "Apple",
  prix: 125794.73,
  ultrabook: true,
  options: [
    "Intel Core i7",
    "SSD",
    "Long life battery"
  ]
})
```

### المنتج 3

``` js
db.produits.insert({
  nom: "Thinkpad X230",
  fabriquant: "Lenovo",
  prix: 114358.74,
  ultrabook: true,
  options: [
    "Intel Core i5",
    "SSD",
    "Long life battery"
  ]
})
```

------------------------------------------------------------------------

## 5. قراءة البيانات (READ)

### عرض كل المنتجات

``` js
db.produits.find().pretty()
```

### عرض أول منتج

``` js
db.produits.findOne()
```

### إيجاد الـ \_id لمنتج معيّن

``` js
db.produits.find(
  { nom: "Thinkpad X230" },
  { _id: 1 }
)
```

### البحث بالـ \_id

``` js
db.produits.find({
  _id: ObjectId("ضع_الـid_هنا")
})
```

### سعر أكبر من قيمة معينة

``` js
db.produits.find({ prix: { $gt: 13723 } })
```

### أول Ultrabook

``` js
db.produits.findOne({ ultrabook: true })
```

### يحتوي الاسم على كلمة

``` js
db.produits.findOne({ nom: /Macbook/ })
```

### يبدأ الاسم بكلمة

``` js
db.produits.find({ nom: /^Macbook/ })
```

------------------------------------------------------------------------

## 6. حذف البيانات (DELETE)

### حذف منتجات Apple

``` js
db.produits.remove({ fabriquant: "Apple" })
```

### حذف منتج بالـ \_id

``` js
db.produits.remove({
  _id: ObjectId("691d74d7dc79adf5624cf081")
})
```
```


------------------------------------------------------------------------

## 7. التحقق النهائي

``` js
db.produits.find().pretty()
```

------------------------------------------------------------------------

## 8. ملاحظة مهمة

MongoDB 2.6 يستعمل `C:\data\db` تلقائيًا إذا كان المجلد موجودًا، حتى لو
لم تستعمل:

``` bat
mongod.exe --dbpath C:\data\db
```
