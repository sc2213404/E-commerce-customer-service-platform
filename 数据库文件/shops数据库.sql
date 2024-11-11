-- 删除数据库，如果已存在
DROP DATABASE IF EXISTS shops;
-- 创建数据库
CREATE DATABASE shops;
-- 使用数据库
USE shops;

-- 创建 User 表
CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(150) NOT NULL
);

-- 创建 ChatHistory 表
CREATE TABLE ChatHistory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_message TEXT,
    bot_response TEXT,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);


-- 插入示例数据到 User 表
INSERT INTO Users VALUES (1,'1', '1');
INSERT INTO Users VALUES (2,'2', '2');

-- 创建 Goods 表
CREATE TABLE Tea_Goods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL
);

-- 创建 Orders 表
CREATE TABLE Tea_Orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    order_date DATETIME NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

-- 创建 OrderGoods 表，用于存储订单与货物的对应关系
CREATE TABLE Tea_OrderGoods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    goods_id INT,
    quantity INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Tea_Orders(id),
    FOREIGN KEY (goods_id) REFERENCES Tea_Goods(id)
);

-- 插入示例数据到 Goods 表
INSERT INTO Tea_Goods (name, description, price, stock) VALUES ('大红袍', '大红袍，产于福建武夷山，属乌龙茶，品质优异。中国特种名茶。其外形条索紧结，色泽绿褐鲜润，冲泡后汤色橙黄明亮，叶片红绿相间。品质最突出之处是香气馥郁有兰花香，香高而持久。', 4900.00, 10);
INSERT INTO Tea_Goods (name, description, price, stock) VALUES ('西湖龙井', '特级西湖龙井茶扁平光滑挺直，色泽嫩绿光润，香气鲜嫩清高，滋味鲜爽甘醇，叶底细嫩呈朵。清明节前采制的龙井茶简称明前龙井，美称女儿红，“院外风荷西子笑，明前龙井女儿红。', 5400.00, 20);
INSERT INTO Tea_Goods (name, description, price, stock) VALUES ('碧螺春', '碧螺春，产于江苏苏州洞庭山，属于绿茶。外形条索纤细，卷曲成螺，满披白毫，色泽银绿隐翠。冲泡后汤色清澈，香气馥郁持久，滋味鲜爽甘醇。', 3800.00, 15);
INSERT INTO Tea_Goods (name, description, price, stock) VALUES ('铁观音', '铁观音，产于福建安溪，属于乌龙茶。外形紧结卷曲，色泽黛绿砂绿，冲泡后汤色金黄明亮，香气浓郁持久，具有独特的兰花香，滋味醇厚甘鲜。', 4600.00, 25);
INSERT INTO Tea_Goods (name, description, price, stock) VALUES ('普洱茶', '普洱茶，产于云南西双版纳，属于黑茶。外形圆紧，色泽乌润。冲泡后汤色红浓明亮，香气独特陈香，滋味醇厚回甘，耐泡度高。', 3200.00, 30);
INSERT INTO Tea_Goods (name, description, price, stock) VALUES ('黄山毛峰', '黄山毛峰，产于安徽黄山，属于绿茶。外形细扁稍曲，状似雀舌，色泽微黄绿润。冲泡后汤色清绿明亮，香气清新持久，滋味鲜醇回甘，叶底嫩绿成朵。', 4100.00, 18);
INSERT INTO Tea_Goods (name, description, price, stock) VALUES ('君山银针', '君山银针，产于湖南岳阳君山，属于黄茶。外形挺直如针，满披白毫，色泽金黄。冲泡后汤色杏黄明亮，香气清高，滋味甘醇，叶底嫩黄明亮。', 5300.00, 12);
INSERT INTO Tea_Goods (name, description, price, stock) VALUES ('六安瓜片', '六安瓜片，产于安徽六安，属于绿茶。外形片形整齐，色泽深绿润泽。冲泡后汤色碧绿清澈，香气清香高爽，滋味鲜醇甘甜，叶底嫩绿明亮。', 3500.00, 22);
INSERT INTO Tea_Goods (name, description, price, stock) VALUES ('武夷岩茶', '武夷岩茶，产于福建武夷山，属于乌龙茶。外形条索紧结，色泽乌润。冲泡后汤色橙黄明亮，香气馥郁持久，具有独特的岩韵，滋味醇厚回甘。', 4800.00, 16);
INSERT INTO Tea_Goods (name, description, price, stock) VALUES ('信阳毛尖', '信阳毛尖，产于河南信阳，属于绿茶。外形细圆紧直，色泽绿润。冲泡后汤色黄绿明亮，香气清香持久，滋味鲜爽甘醇，叶底嫩绿明亮。', 3700.00, 20);
INSERT INTO Tea_Goods (name, description, price, stock) VALUES ('安吉白茶', '安吉白茶，产于浙江安吉，属于绿茶。外形细秀显芽，色泽翠绿，冲泡后汤色清澈明亮，香气清幽，滋味鲜爽甘醇。', 4500.00, 14);
INSERT INTO Tea_Goods (name, description, price, stock) VALUES ('洞庭碧螺春', '洞庭碧螺春，产于江苏苏州洞庭山，属于绿茶。外形卷曲如螺，色泽碧绿，冲泡后汤色碧绿清澈，香气浓郁持久，滋味鲜爽甘醇。', 5000.00, 10);
INSERT INTO Tea_Goods (name, description, price, stock) VALUES ('龙井43号', '龙井43号，产于浙江杭州西湖，属于绿茶。外形扁平挺直，色泽嫩绿，冲泡后汤色嫩绿明亮，香气清高持久，滋味鲜爽甘醇。', 5200.00, 15);
INSERT INTO Tea_Goods (name, description, price, stock) VALUES ('桂花龙井', '桂花龙井，产于浙江杭州，属于花茶。外形扁平光滑，色泽黄绿，冲泡后汤色清澈明亮，桂花香气浓郁，滋味甘醇。', 4900.00, 18);
INSERT INTO Tea_Goods (name, description, price, stock) VALUES ('金骏眉', '金骏眉，产于福建武夷山，属于红茶。外形细长紧结，色泽金黄，冲泡后汤色金黄明亮，香气高爽持久，滋味甘甜醇厚。', 6000.00, 8);
INSERT INTO Tea_Goods (name, description, price, stock) VALUES ('祁门红茶', '祁门红茶，产于安徽祁门，属于红茶。外形细紧，色泽乌润，冲泡后汤色红亮，香气馥郁持久，滋味醇厚回甘。', 4300.00, 20);
INSERT INTO Tea_Goods (name, description, price, stock) VALUES ('英德红茶', '英德红茶，产于广东英德，属于红茶。外形紧结圆润，色泽乌黑油润，冲泡后汤色红艳明亮，香气高长，滋味浓强鲜爽。', 4100.00, 25);
INSERT INTO Tea_Goods (name, description, price, stock) VALUES ('毛峰茶', '毛峰茶，产于安徽黄山，属于绿茶。外形细嫩稍曲，色泽绿润，冲泡后汤色清澈，香气清高持久，滋味鲜爽甘醇。', 3800.00, 22);
INSERT INTO Tea_Goods (name, description, price, stock) VALUES ('洞庭碧螺春特级', '洞庭碧螺春特级，产于江苏苏州洞庭山，属于绿茶。外形卷曲如螺，色泽碧绿，冲泡后汤色碧绿清澈，香气浓郁持久，滋味鲜爽甘醇。', 5200.00, 10);
INSERT INTO Tea_Goods (name, description, price, stock) VALUES ('白毫银针', '白毫银针，产于福建福鼎，属于白茶。外形纤细如针，色泽银白，冲泡后汤色淡黄清澈，香气清幽，滋味鲜爽甘醇。', 5500.00, 12);

-- 插入示例数据到 Orders 表
INSERT INTO Tea_Orders (user_id, order_date, total_amount) VALUES (1, NOW(), 2300.00);

-- 插入示例数据到 OrderGoods 表
INSERT INTO Tea_OrderGoods (order_id, goods_id, quantity) VALUES (1, 1, 1); -- 一个订单包含一台Laptop
INSERT INTO Tea_OrderGoods (order_id, goods_id, quantity) VALUES (1, 2, 1); -- 同一个订单还包含一台Smartphone

-- 创建 Goods 表
CREATE TABLE Book_Goods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL
);

-- 创建 Orders 表
CREATE TABLE Book_Orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    order_date DATETIME NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

-- 创建 OrderGoods 表，用于存储订单与货物的对应关系
CREATE TABLE Book_OrderGoods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    goods_id INT,
    quantity INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Book_Orders(id),
    FOREIGN KEY (goods_id) REFERENCES Book_Goods(id)
);

-- 插入示例数据到 Goods 表
INSERT INTO Book_Goods (name, description, price, stock) VALUES ('红楼梦', '四大名著之一', 399.00, 10);
INSERT INTO Book_Goods (name, description, price, stock) VALUES ('悲惨世界', '法国作家维克多·雨果创作的一部长篇小说', 149.00, 20);
INSERT INTO Book_Goods (name, description, price, stock) VALUES ('西游记', '四大名著之一', 299.00, 15);
INSERT INTO Book_Goods (name, description, price, stock) VALUES ('水浒传', '四大名著之一', 349.00, 12);
INSERT INTO Book_Goods (name, description, price, stock) VALUES ('三国演义', '四大名著之一', 399.00, 18);
INSERT INTO Book_Goods (name, description, price, stock) VALUES ('百年孤独', '哥伦比亚作家加西亚·马尔克斯的代表作', 129.00, 25);
INSERT INTO Book_Goods (name, description, price, stock) VALUES ('飘', '美国作家玛格丽特·米切尔创作的长篇小说', 159.00, 30);
INSERT INTO Book_Goods (name, description, price, stock) VALUES ('简爱', '英国作家夏洛蒂·勃朗特创作的长篇小说', 99.00, 40);
INSERT INTO Book_Goods (name, description, price, stock) VALUES ('傲慢与偏见', '英国作家简·奥斯汀的代表作', 89.00, 35);
INSERT INTO Book_Goods (name, description, price, stock) VALUES ('战争与和平', '俄国作家列夫·托尔斯泰创作的长篇小说', 199.00, 22);
INSERT INTO Book_Goods (name, description, price, stock) VALUES ('哈利·波特与魔法石', '英国作家J.K.罗琳创作的奇幻小说', 59.00, 50);
INSERT INTO Book_Goods (name, description, price, stock) VALUES ('鲁滨逊漂流记', '英国作家丹尼尔·笛福创作的长篇小说', 79.00, 28);
INSERT INTO Book_Goods (name, description, price, stock) VALUES ('变形记', '捷克作家卡夫卡创作的中篇小说', 69.00, 15);
INSERT INTO Book_Goods (name, description, price, stock) VALUES ('弗兰肯斯坦', '英国作家玛丽·雪莱创作的长篇小说', 109.00, 12);
INSERT INTO Book_Goods (name, description, price, stock) VALUES ('老人与海', '美国作家海明威创作的中篇小说', 79.00, 38);
INSERT INTO Book_Goods (name, description, price, stock) VALUES ('双城记', '英国作家查尔斯·狄更斯创作的长篇小说', 99.00, 26);
INSERT INTO Book_Goods (name, description, price, stock) VALUES ('呼啸山庄', '英国作家艾米莉·勃朗特创作的长篇小说', 109.00, 18);

-- 插入示例数据到 Orders 表
INSERT INTO Tea_Orders (user_id, order_date, total_amount) VALUES (1, NOW(), 2300.00);

-- 插入示例数据到 OrderGoods 表
INSERT INTO Tea_OrderGoods (order_id, goods_id, quantity) VALUES (1, 1, 1); -- 一个订单包含一台Laptop
INSERT INTO Tea_OrderGoods (order_id, goods_id, quantity) VALUES (1, 2, 1); -- 同一个订单还包含一台Smartphone

-- 创建 Goods 表
CREATE TABLE Coffee_Goods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL
);

-- 创建 Orders 表
CREATE TABLE Coffee_Orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    order_date DATETIME NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

-- 创建 OrderGoods 表，用于存储订单与货物的对应关系
CREATE TABLE Coffee_OrderGoods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    goods_id INT,
    quantity INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Coffee_Orders(id),
    FOREIGN KEY (goods_id) REFERENCES Coffee_Goods(id)
);

-- 插入示例数据到 Goods 表
INSERT INTO Coffee_Goods (name, description, price, stock) VALUES ('美式', '苦', 29.00, 10);
INSERT INTO Coffee_Goods (name, description, price, stock) VALUES ('拿铁', '不那么苦', 29.00, 20);
INSERT INTO Coffee_Goods (name, description, price, stock) VALUES ('卡布奇诺', '浓郁而带有奶泡', 35.00, 15);
INSERT INTO Coffee_Goods (name, description, price, stock) VALUES ('摩卡', '巧克力风味', 38.00, 18);
INSERT INTO Coffee_Goods (name, description, price, stock) VALUES ('玛奇朵', '香甜奶油味', 40.00, 12);
INSERT INTO Coffee_Goods (name, description, price, stock) VALUES ('浓缩咖啡', '强烈而浓厚', 30.00, 25);
INSERT INTO Coffee_Goods (name, description, price, stock) VALUES ('冰美式', '冰凉苦涩', 28.00, 20);
INSERT INTO Coffee_Goods (name, description, price, stock) VALUES ('冰拿铁', '冰凉奶香', 32.00, 22);
INSERT INTO Coffee_Goods (name, description, price, stock) VALUES ('白咖啡', '柔和奶香', 35.00, 17);
INSERT INTO Coffee_Goods (name, description, price, stock) VALUES ('焦糖玛奇朵', '香甜焦糖味', 42.00, 14);
INSERT INTO Coffee_Goods (name, description, price, stock) VALUES ('抹茶拿铁', '抹茶风味', 36.00, 19);
INSERT INTO Coffee_Goods (name, description, price, stock) VALUES ('澳白', '浓郁奶泡', 33.00, 16);
INSERT INTO Coffee_Goods (name, description, price, stock) VALUES ('短笛', '浓缩咖啡的一种，口感强烈', 33.00, 15);
INSERT INTO Coffee_Goods (name, description, price, stock) VALUES ('平白', '奶泡绵密，口感顺滑', 34.00, 18);
INSERT INTO Coffee_Goods (name, description, price, stock) VALUES ('冰卡布奇诺', '冰凉浓郁，奶泡丰富', 38.00, 20);
INSERT INTO Coffee_Goods (name, description, price, stock) VALUES ('冰摩卡', '冰凉巧克力风味', 40.00, 22);
INSERT INTO Coffee_Goods (name, description, price, stock) VALUES ('美式（无咖啡因）', '不含咖啡因，口感纯正', 30.00, 12);
INSERT INTO Coffee_Goods (name, description, price, stock) VALUES ('香草拿铁', '香草风味，甜美可口', 37.00, 16);
INSERT INTO Coffee_Goods (name, description, price, stock) VALUES ('意式浓缩', '经典意大利风味，浓烈醇厚', 32.00, 25);
INSERT INTO Coffee_Goods (name, description, price, stock) VALUES ('冰焦糖玛奇朵', '冰凉香甜，焦糖风味', 45.00, 14);
INSERT INTO Coffee_Goods (name, description, price, stock) VALUES ('冰抹茶拿铁', '冰凉抹茶风味', 39.00, 19);
INSERT INTO Coffee_Goods (name, description, price, stock) VALUES ('柠檬美式', '清新柠檬香气，苦中带酸', 35.00, 16);

-- 插入示例数据到 Orders 表
INSERT INTO Coffee_Orders (user_id, order_date, total_amount) VALUES (1, NOW(), 2300.00);

-- 插入示例数据到 OrderGoods 表
INSERT INTO Coffee_OrderGoods (order_id, goods_id, quantity) VALUES (1, 1, 1); -- 一个订单包含一台Laptop
INSERT INTO Coffee_OrderGoods (order_id, goods_id, quantity) VALUES (1, 2, 1); -- 同一个订单还包含一台Smartphoneaddresscoffeesfaq