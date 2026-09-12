# sklearn-এর linear_model module থেকে LinearRegression class নিয়ে আসছি
from sklearn.linear_model import LinearRegression

# hours = Input/Feature
# এখানে আমরা model-কে বলছি: 1 ঘণ্টা পড়লে, 2 ঘণ্টা পড়লে, 3 ঘণ্টা পড়লে ইত্যাদি কত marks পাওয়া গেছে
# প্রতিটি value-এর ভিতরে [] আছে কারণ sklearn সাধারণত..input-কে 2D format-এ নেয়।
# [1] = 1 ঘণ্টা
# [2] = 2 ঘণ্টা
# [3] = 3 ঘণ্টা
# [5] = 5 ঘণ্টা
# [6] = 6 ঘণ্টা
hours = [[1], [2], [3], [5], [6]]

# marks = Output/Target
# উপরের hours-এর corresponding marks:
# 1 ঘণ্টা → 50
# 2 ঘণ্টা → 60
# 3 ঘণ্টা → 70
# 5 ঘণ্টা → 90
# 6 ঘণ্টা → 95
marks = [50, 60, 70, 90, 95]

# LinearRegression-এর একটা model/object তৈরি করছি.. এখনো model কিছু শেখেনি। শুধু একটা empty Linear Regression model তৈরি হয়েছে।
model = LinearRegression()

# fit() দিয়ে model-কে training data দিচ্ছি
# hours = Input/X, marks = Output/y
# অর্থাৎ model এখন এই relationship শেখার চেষ্টা করবে:
# hours → marks
# Model বুঝতে চেষ্টা করবে: "পড়ার ঘণ্টা বাড়লে marks কীভাবে বাড়ছে?"
model.fit(hours, marks)

# এখন model-কে নতুন একটা input দিচ্ছি: 4 ঘণ্টা পড়লে কত marks হতে পারে?
# model.predict() prediction করার জন্য ব্যবহার হয়। [[4]] কারণ নতুন input-টাও 2D format-এ দিতে হয়।
predicted = model.predict([[4]])

# predicted-এর ভিতরে একটা value থাকবে।
# predicted[0] → সেই প্রথম prediction
# :.2f → decimal-এর পর 2টা সংখ্যা দেখাবে.. যেমন: 78.50
print(f"4 ghonta porle pabe: {predicted[0]:.2f} marks")

# এবার model-কে আরেকটা নতুন input দিচ্ছি: 10 ঘণ্টা পড়লে কত marks হতে পারে?
predicted2 = model.predict([[10]])

# 10 ঘণ্টার prediction print করছি
print(f"10 ghonta porle pabe: {predicted2[0]:.2f} marks")