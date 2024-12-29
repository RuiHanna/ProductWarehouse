-- MySQL dump 10.13  Distrib 5.7.31, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: warehouse
-- ------------------------------------------------------
-- Server version	5.7.31

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `client`
--

DROP TABLE IF EXISTS `client`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `client` (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `cname` varchar(20) NOT NULL,
  `type` varchar(20) DEFAULT NULL,
  `contacts` varchar(20) NOT NULL,
  `contact_number` varchar(20) NOT NULL,
  `address` varchar(20) DEFAULT NULL,
  `remarks` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`cid`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client`
--

LOCK TABLES `client` WRITE;
/*!40000 ALTER TABLE `client` DISABLE KEYS */;
INSERT INTO `client` VALUES (1,'小米','有限责任公司','雷军','11112222333','北京市昌平区南口镇南涧路29号','永远相信美好的事情即将发生'),(2,'万集科技','有限责任公司','翟军','12121212321','北京市北京经济技术开发区',''),(3,'格力集团','股份有限公司','董明珠','12121212123','广东省珠海市前山金鸡西路6号','让世界爱上中国造'),(4,'美的集团','股份有限公司','方洪波','12121321123','广东省佛山市顺德区北滘镇美的大道6号',''),(5,'华为','技术有限公司','任正非','12121321321','广东省深圳市龙岗区坂田华为总部办公楼','构建万物互联的智能世界');
/*!40000 ALTER TABLE `client` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product` (
  `pid` int(11) NOT NULL AUTO_INCREMENT,
  `pname` varchar(20) NOT NULL,
  `specification` varchar(20) DEFAULT NULL,
  `reference_price` float DEFAULT NULL,
  `maxlim` int(11) DEFAULT NULL,
  `minlim` int(11) DEFAULT NULL,
  PRIMARY KEY (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (1,'螺丝','1mm',0.5,50000,1000),(2,'螺丝','2mm',0.5,50000,1000),(3,'螺丝','3mm',0.5,50000,1000),(4,'螺丝','5mm',0.5,50000,1000),(5,'螺母','1mm',0.5,50000,1000),(6,'螺母','2mm',0.5,50000,1000),(7,'螺母','3mm',0.5,50000,1000),(8,'螺母','5mm',0.5,50000,1000),(9,'螺栓','1mm',0.5,50000,1000),(10,'螺栓','2mm',0.5,50000,1000),(11,'螺栓','3mm',0.5,50000,1000);
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `uname` varchar(20) NOT NULL,
  `pwd` varchar(200) NOT NULL,
  `auth` smallint(6) NOT NULL,
  `address` varchar(50) NOT NULL,
  `remarks` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'杨蕊菡','scrypt:32768:8:1$X0fu6elyF86ESbxd$f39450b1370d4d6eff19b2125e59e207586484012eb517634f461f1db65c11dd7e04df543dc218b3275bc3118d8fbea1d66c324c5256c7b565f7a934d01b6081',0,'2022040068@buct.edu.cn','超级管理员，可修改管理员权限'),(2,'冯家宁','scrypt:32768:8:1$VUeac51aQxsivIPB$47aab72e019ba3c00e1db5c3db11f7d0feac57f1991c5d883fee4c8af28e782a971bc222de40337649b3b45d5abb8f72787e5ebba6573e45f59c14b144155bae',1,'2022040059@buct.edu.cn','管理员，负责客户管理、产品管理、仓库管理'),(3,'刘琳','scrypt:32768:8:1$EQjTlbdCuhtnnv03$2c45a5b0c4912c4c9c64c9811136109ff187700eb0ed64ff011a99d95d5d7ac81f8afdef86649e1e29fd72f96f0be3d5bebc818a757bf24239e3bfff41672936',1,'2022040062@buct.edu.cn','管理员'),(4,'陈嘉欣','scrypt:32768:8:1$X7NozRH4oKy4uODM$35a2955d52db70138cb20633094f1ba59bd0fe9b885e96c487d65a2e3f039ebfed6187de75a2edf6b0ca8e15162227f39a010640903764191ffaac937c849462',0,'2022040066@buct.edu.cn','超级管理员');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `warehouse`
--

DROP TABLE IF EXISTS `warehouse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `warehouse` (
  `wid` int(11) NOT NULL AUTO_INCREMENT,
  `wname` varchar(20) NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`wid`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `warehouse`
--

LOCK TABLES `warehouse` WRITE;
/*!40000 ALTER TABLE `warehouse` DISABLE KEYS */;
INSERT INTO `warehouse` VALUES (1,'北京昌平仓库','保存螺丝零件'),(2,'北京朝阳仓库','保存螺栓零件'),(3,'北京顺义仓库','保存螺母零件'),(4,'北京海淀仓库','作为备用仓库'),(5,'广东佛山仓库','保存螺丝零件'),(6,'天津滨海新区仓库','保存螺栓零件'),(7,'河北廊坊仓库','保存螺母零件');
/*!40000 ALTER TABLE `warehouse` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-29 21:12:12
