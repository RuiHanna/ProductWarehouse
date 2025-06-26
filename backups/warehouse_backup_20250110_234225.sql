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
INSERT INTO `client` VALUES (1,'xx','有限责任公司','XX','11112222333','xx市xx区xx镇xx路xx号',''),(2,'xxxx','有限责任公司','XX','12121212321','xx市xx经济技术开发区',''),(3,'xxxxx','股份有限公司','XXX','12121212123','xx省xx市xxxx路x号',''),(4,'xxxxxx','股份有限公司','XXX','12121321123','xx省xx市xx区xxxx大道x号',''),(5,'xxxxxxxx','技术有限公司','XXX','12121321321','xx省xx市xx区xx总部办公楼','');
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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'杨蕊菡','scrypt:32768:8:1$JVUKLLbpY7iuvdU1$0fd78e242d4adc4eba40bb315fda2f77a94ef40e1c0fc777e7063ff99165ad80f85de6f96c27054be617c944b1118e824520f135e00b46ad0078e39053bdf7fd',0,'2022040068@buct.edu.cn','超级管理员，可修改管理员权限'),(4,'陈嘉欣','scrypt:32768:8:1$X7NozRH4oKy4uODM$35a2955d52db70138cb20633094f1ba59bd0fe9b885e96c487d65a2e3f039ebfed6187de75a2edf6b0ca8e15162227f39a010640903764191ffaac937c849462',0,'2022040066@buct.edu.cn','超级管理员'),(5,'陈柯翰','scrypt:32768:8:1$IGQy25wrg8LeybMd$cd35bc85f809c9b069654ab29b164f5f3f8480c8fa233cdb20520a25c89442060ac3e8f142d43fef0a6453e3c9064fddd0d07be44e7c3ad5b5331d747d243fe8',0,'2022130101022@std.uestc.edu.cn','秋刀鱼'),(7,'xxx','scrypt:32768:8:1$EATnqTywiXPfmHG5$dace590b6cfefc55aa8ad894e1f72cdfedd9f4803d627f6afcbf046adcf8f98da61e0477554fe1dbbe84eb0a5a215e0e599cb57f8a513811d202651d7d46ed05',1,'2916436728@qq.com',''),(8,'xx','scrypt:32768:8:1$HRHtnLy4ffbrzvia$6c8425add04ee314d85d36d8b4fe7768eb5908ee520a3b4ee7e9eb39110b64978c87e7e8a838b675dd53aeeda24b7086ea392e27ec5dad96196036786b8ba47a',1,'2916436728@qq.com',''),(9,'xxxx','scrypt:32768:8:1$OrBJYhaFlHNGbhWq$a15c891a3f162dd4d4b6bc44be871054ad0d5aafc168bad7ef304afa2c0c199eaa9293ecfd55c937fe0af1f582f5f30939f147b0f5468c1c5e0d8649bd70e0b7',0,'2916436728@qq.com','');
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
INSERT INTO `warehouse` VALUES (1,'xxxx仓库','保存螺丝零件'),(2,'xxxx仓库','保存螺栓零件'),(3,'xxxx仓库','保存螺母零件'),(4,'xxxx仓库','作为备用仓库'),(5,'xxxx仓库','保存螺丝零件'),(6,'xxxxxx仓库','保存螺栓零件'),(7,'xxxx仓库','保存螺母零件');
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

-- Dump completed on 2025-01-10 23:42:25
