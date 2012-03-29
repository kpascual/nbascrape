-- MySQL dump 10.13  Distrib 5.1.61, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: nba
-- ------------------------------------------------------
-- Server version	5.1.61-0ubuntu0.11.10.1

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
-- Table structure for table `shot_type_nbacom`
--

DROP TABLE IF EXISTS `shot_type_nbacom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shot_type_nbacom` (
  `id` int(11) NOT NULL DEFAULT '0',
  `nbacom_id` int(11) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `shot_group` varchar(100) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shot_type_nbacom`
--

LOCK TABLES `shot_type_nbacom` WRITE;
/*!40000 ALTER TABLE `shot_type_nbacom` DISABLE KEYS */;
INSERT INTO `shot_type_nbacom` VALUES (1,0,'No Shot',''),(2,1,'Jump Shot','Jump Shot'),(3,2,'Running Jump Shot','Jump Shot'),(4,3,'Hook Shot','Jump Shot'),(5,4,'Tip Shot','Tip-in'),(6,5,'Layup Shot','Lay-up'),(7,6,'Driving Layup Shot','Lay-up'),(8,7,'Dunk Shot','Dunk'),(9,8,'Slam Dunk Shot','Dunk'),(10,9,'Driving Dunk Shot','Dunk'),(11,40,'Layup','Lay-up'),(12,41,'Running Layup','Lay-up'),(13,42,'Driving Layup','Lay-up'),(14,43,'Alley Oop Layup','Lay-up'),(15,44,'Reverse Layup','Lay-up'),(16,45,'Jump Shot','Jump Shot'),(17,46,'Running Jump','Jump Shot'),(18,47,'Turnaround Jump','Jump Shot'),(19,48,'Dunk','Dunk'),(20,49,'Driving Dunk','Dunk'),(21,50,'Running Dunk','Dunk'),(22,51,'Reverse Dunk','Dunk'),(23,52,'Alley Oop Dunk','Dunk'),(24,53,'Tip-In','Tip-in'),(25,54,'Running Tip-In','Tip-in'),(26,55,'Hook Shot','Jump Shot'),(27,56,'Running Hook Shot','Jump Shot'),(28,57,'Driving Hook Shot','Jump Shot'),(29,58,'Turnaround Hook Shot','Jump Shot'),(30,59,'Finger Roll','Lay-up'),(31,60,'Running Finger Roll','Lay-up'),(32,61,'Driving Finger Roll','Lay-up'),(33,62,'Turnaround Finger Roll','Lay-up'),(34,63,'Fade Away','Jump Shot'),(35,64,'Follow Up Dunk','Dunk'),(36,65,'Jump Hook','Jump Shot'),(37,66,'Jump Bank','Jump Shot'),(38,67,'Hook Bank','Jump Shot'),(39,71,'Finger Roll Layup','Lay-up'),(40,72,'Putback Layup','Lay-up'),(41,73,'Driving Reverse Layup','Lay-up'),(42,74,'Running Reverse Layup','Lay-up'),(43,75,'Driving Finger Roll Layup','Lay-up'),(44,76,'Running Finger Roll Layup','Lay-up'),(45,77,'Driving Jump Shot','Jump Shot'),(46,78,'Floating Jump Shot','Jump Shot'),(47,79,'Pullup Jump Shot','Jump Shot'),(48,80,'Step Back Jump Shot','Jump Shot'),(49,81,'Pullup Bank Shot','Jump Shot'),(50,82,'Driving Bank Shot','Jump Shot'),(51,83,'Fade Away Bank Shot','Jump Shot'),(52,84,'Running Bank Shot','Jump Shot'),(53,85,'Turnaround Bank Shot','Jump Shot'),(54,86,'Turnaround Fade Away Shot','Jump Shot'),(55,87,'Putback Dunk','Dunk'),(56,88,'Driving Slam Dunk','Dunk'),(57,89,'Reverse Slam Dunk','Dunk'),(58,90,'Running Slam Dunk','Dunk'),(59,91,'Putback Reverse Dunk','Dunk'),(60,92,'Putback Slam Dunk','Dunk'),(61,93,'Driving Bank Hook','Jump Shot'),(62,94,'Jump Bank Hook','Jump Shot'),(63,95,'Running Bank Hook','Jump Shot'),(64,96,'Turnaround Bank Hook','Jump Shot');
/*!40000 ALTER TABLE `shot_type_nbacom` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shot_type_cbssports`
--

DROP TABLE IF EXISTS `shot_type_cbssports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shot_type_cbssports` (
  `id` int(11) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `is_freethrow` tinyint(4) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shot_type_cbssports`
--

LOCK TABLES `shot_type_cbssports` WRITE;
/*!40000 ALTER TABLE `shot_type_cbssports` DISABLE KEYS */;
INSERT INTO `shot_type_cbssports` VALUES (0,'Shot',0),(1,'Jump Shot',0),(2,'Running Jump',0),(3,'Hook Shot',0),(5,'Layup',0),(6,'Driving Layup',0),(7,'Dunk Shot',0),(8,'Slam Dunk',0),(9,'Driving Dunk',0),(10,'Free Throw',1),(11,'1st of 2 Free Throws',1),(12,'2nd of 2 Free Throws',1),(13,'1st of 3 Free Throws',1),(14,'2nd of 3 Free Throws',1),(15,'3rd of 3 Free Throws',1),(16,'Technical Free Throw',1),(17,'1st of 2 Free Throws',1),(18,'2nd of 2 Free Throws',1),(19,'Finger Roll',0),(20,'Reverse Layup',0),(21,'Turnaround Jump Shot',0),(22,'Fadeaway Jump Shot',0),(23,'Floating Jump Shot',0),(24,'Leaning Jump Shot',0),(25,'Mini Hook Shot',0);
/*!40000 ALTER TABLE `shot_type_cbssports` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `play_espn`
--

DROP TABLE IF EXISTS `play_espn`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `play_espn` (
  `id` int(11) NOT NULL,
  `re` varchar(1000) NOT NULL,
  `name` varchar(1000) NOT NULL,
  `is_shot` tinyint(1) DEFAULT NULL,
  `is_freethrow` tinyint(4) DEFAULT NULL,
  `is_shot_made` tinyint(4) NOT NULL DEFAULT '0',
  `priority` smallint(6) DEFAULT NULL,
  `has_player2` tinyint(4) DEFAULT NULL,
  `has_player1` tinyint(4) DEFAULT NULL,
  `is_on_floor` tinyint(4) DEFAULT NULL,
  `is_rebound` tinyint(4) DEFAULT '0',
  `is_foul` tinyint(4) DEFAULT '0',
  `is_turnover` tinyint(4) DEFAULT '0',
  `is_assist` tinyint(4) DEFAULT '0',
  `points_possible` tinyint(4) DEFAULT NULL,
  `points_converted` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `play_espn`
--

LOCK TABLES `play_espn` WRITE;
/*!40000 ALTER TABLE `play_espn` DISABLE KEYS */;
INSERT INTO `play_espn` VALUES (1,'<b>(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+makes\\s+technical\\s+free\\s+throw</b>','<b><player> makes technical free throw</b>',0,1,1,1,0,0,1,0,0,0,0,0,0),(2,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+misses\\s+(?P<shot_type>[a-zA-Z-\\s]+)','<player> misses <shot_type>',1,0,0,12,0,0,1,0,0,0,0,2,0),(3,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+misses\\s+(?P<distance>[0-9]{1,2})-foot\\s+(?P<shot_type>[a-zA-Z-\\s]+)','<player> misses <distance>-foot <shot_type>',1,0,0,3,0,0,1,0,0,0,0,2,0),(4,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+misses\\s+free\\s+throw\\s+1\\s+of\\s+1','<player> misses free throw 1 of 1',0,1,0,1,0,0,1,0,0,0,0,0,0),(5,'Jumpball:\\s+(?P<player1>[a-zA-Z-\\\'\\s\\.]+)\\s+vs\\.\\s+(?P<player2>[a-zA-Z-\\\'\\s\\.]+)\\s+\\((?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+gains\\s+possession\\)','Jumpball: <player1> vs. <player2> (<player> gains possession)',0,0,0,6,1,1,1,0,0,0,0,0,0),(6,'<b>(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+makes\\s+driving\\s+layup\\s+((?P<assist_player>[a-zA-Z-\\\'\\s\\.]+)\\s+assists)</b>','<b><player> makes driving layup (<assist_player> assists)</b>',1,0,1,11,0,0,1,0,0,0,1,2,2),(7,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+timeout','<player> timeout',0,0,0,11,0,0,1,0,0,0,0,0,0),(8,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+(?P<foul_type>[a-zA-Z-\\\'s\\.]+)\\s+foul\\s+\\((?P<player2>[a-zA-Z-\\\'\\s\\.]+)\\s+draws\\s+the\\s+foul\\)','<player> <foul_type> foul (<player2> draws the foul)',0,0,0,12,1,0,1,0,1,0,0,0,0),(9,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+traveling','<player> traveling',0,0,0,4,0,0,1,0,0,1,0,0,0),(10,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+misses\\s+three\\s+point\\s+jumper','<player> misses three point jumper',1,0,0,1,0,0,1,0,0,0,0,3,0),(11,'<b>(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+makes\\s+dunk\\s+((?P<assist_player>[a-zA-Z-\\\'\\s\\.]+)\\s+assists)</b>','<b><player> makes dunk (<assist_player> assists)</b>',1,0,1,11,0,0,1,0,0,0,1,2,2),(12,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+(?P<foul_type>[a-zA-Z-\\\'\\s\\.]+)\\s+foul\\s+\\((?P<foul_info>[0-9a-zA-Z-\\\'\\s\\.]+)\\)','<player> <foul_type> foul (<foul_info>)',0,0,0,11,0,0,1,0,1,0,0,0,0),(13,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+loose\\s+ball\\s+foul\\s+\\((?P<player2>[a-zA-Z-\\\'\\s\\.]+)\\s+draws\\s+the\\s+foul\\)','<player> loose ball foul (<player2> draws the foul)',0,0,0,11,1,0,1,0,1,0,0,0,0),(14,'<b>(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+makes\\s+two\\s+point\\s+shot\\s+((?P<assist_player>[a-zA-Z-\\\'\\s\\.]+)\\s+assists)</b>','<b><player> makes two point shot (<assist_player> assists)</b>',1,0,1,11,0,0,1,0,0,0,1,2,2),(15,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+offensive\\s+foul\\s+\\((?P<player2>[a-zA-Z-\\\'\\s\\.]+)\\s+draws\\s+the\\s+foul\\)','<player> offensive foul (<player2> draws the foul)',0,0,0,11,1,0,1,0,1,0,0,0,0),(16,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+offensive\\s+team\\s+rebound','Offensive team rebound (<player>)',0,0,0,11,0,0,1,1,0,0,0,0,0),(17,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+misses\\s+jumper','<player> misses jumper',1,0,0,11,0,0,1,0,0,0,0,2,0),(18,'<b>(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+makes\\s+free\\s+throw\\s+1\\s+of\\s+1</b>','<b><player> makes free throw 1 of 1</b>',0,1,1,1,0,0,1,0,0,0,0,0,0),(19,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+defensive\\s+team\\s+rebound','Defensive team rebound (<player>)',0,0,0,11,0,0,1,1,0,0,0,0,0),(20,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+bad\\s+pass','<player> bad pass',0,0,0,4,0,0,1,0,0,1,0,0,0),(21,'<b>(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+makes\\s+(?P<distance>[0-9]{1,2})-foot\\s+two\\s+point\\s+shot\\s+((?P<assist_player>[a-zA-Z-\\\'\\s\\.]+)\\s+assists)</b>','<b><player> makes <distance>-foot two point shot (<assist_player> assists)</b>',1,0,1,11,0,0,1,0,0,0,1,2,2),(22,'(?P<player2>[a-zA-Z-\\\'\\s\\.]+)\\s+blocks\\s+(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\\'s\\s+(?P<shot_type>[a-zA-Z-\\s]+)','<player2> blocks <player>\'s <shot_type>',1,0,0,11,1,0,1,0,0,0,0,2,0),(23,'(?P<player2>[a-zA-Z-\\\'\\s\\.]+)\\s+blocks\\s+(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\\'s\\s+(?P<distance>[0-9]{1,2})-foot\\s+(?P<shot_type>[a-zA-Z-\\s]+)','<player2> blocks <player>\'s <distance>-foot <shot_type>',1,0,0,5,1,0,1,0,0,0,0,2,0),(24,'<b>(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+makes\\s+layup</b>','<b><player> makes layup</b>',1,0,1,10,0,0,1,0,0,0,0,2,2),(25,'<b>(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+makes\\s+driving\\s+layup</b>','<b><player> makes driving layup</b>',1,0,1,10,0,0,1,0,0,0,0,2,2),(26,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+misses\\s+free\\s+throw\\s+2\\s+of\\s+2','<player> misses free throw 2 of 2',0,1,0,1,0,0,1,0,0,0,0,0,0),(27,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+misses\\s+free\\s+throw\\s+1\\s+of\\s+2','<player> misses free throw 1 of 2',0,1,0,1,0,0,1,0,0,0,0,0,0),(28,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+misses\\s+(?P<distance>[0-9]{1,2})-foot\\s+two\\s+point\\s+shot','<player> misses <distance>-foot two point shot',1,0,0,11,0,0,1,0,0,0,0,2,0),(29,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+misses\\s+layup','<player> misses layup',1,0,0,1,0,0,1,0,0,0,0,2,0),(30,'<b>(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+makes\\s+(?P<distance>[0-9]{1,2})-foot\\s+(?P<shot_type>[a-zA-Z-\\s]+)</b>','<b><player> makes <distance>-foot <shot_type></b>',1,0,1,3,0,0,1,0,0,0,0,2,2),(31,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+turnover','<player> turnover',0,0,0,4,0,0,1,0,0,1,0,0,0),(32,'<b>(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+makes\\s+(?P<distance>[0-9]{1,2})-foot\\s+(?P<shot_type>[a-zA-Z-\\s]+)\\s+\\((?P<assist_player>[a-zA-Z-\\\'\\s\\.]+)\\s+assists\\)</b>','<b><player> makes <distance>-foot <shot_type> (<assist_player> assists)</b>',1,0,1,3,0,0,1,0,0,0,1,2,2),(33,'<b>(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+makes\\s+(?P<shot_type>[a-zA-Z-\\s]+)</b>','<b><player> makes <shot_type></b>',1,0,1,12,0,0,1,0,0,0,0,2,2),(34,'<b>(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+makes\\s+(?P<shot_type>[a-zA-Z-\\s]+)\\s+\\((?P<assist_player>[a-zA-Z-\\\'\\s\\.]+)\\s+assists\\)</b>','<b><player> makes <shot_type> (<assist_player> assists)</b>',1,0,1,3,0,0,1,0,0,0,1,2,2),(35,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+lost\\s+ball\\s+\\((?P<player2>[a-zA-Z-\\\'\\s\\.]+)\\s+steals\\)','<player> lost ball (<player2> steals)',0,0,0,3,1,0,1,0,0,1,0,0,0),(36,'<b>(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+makes\\s+(?P<distance>[0-9]{1,2})-foot\\s+two\\s+point\\s+shot</b>','<b><player> makes <distance>-foot two point shot</b>',1,0,1,11,0,0,1,0,0,0,0,2,2),(92,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+(?P<foul_type>(shooting|offensive|personal|loose\\sball|clear\\spath))\\s+foul\\s+\\((?P<player2>[a-zA-Z-\\\'\\s\\.]+)\\s+draws\\s+the\\s+foul\\)','<player> <foul_type> foul (<player2> draws the foul)',0,0,0,6,1,0,1,0,1,0,0,0,0),(38,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+bad\\s+pass\\s+\\((?P<player2>[a-zA-Z-\\\'\\s\\.]+)\\s+steals\\)','<player> bad pass (<player2> steals)',0,0,0,11,1,0,1,0,0,1,0,0,0),(39,'<b>(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+makes\\s+(?P<distance>[0-9]{1,2})-foot\\s+jumper\\s+((?P<assist_player>[a-zA-Z-\\\'\\s\\.]+)\\s+assists)</b>','<b><player> makes <distance>-foot jumper (<assist_player> assists)</b>',1,0,1,3,0,0,1,0,0,0,1,2,2),(40,'<b>(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+makes\\s+(?P<distance>[0-9]{1,2})-foot\\s+three\\s+point\\s+jumper\\s+\\((?P<assist_player>[a-zA-Z-\\\'\\s\\.]+)\\s+assists\\)</b>','<b><player> makes <distance>-foot three point jumper (<assist_player> assists)</b>',1,0,1,2,0,0,1,0,0,0,1,3,3),(41,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+personal\\s+foul\\s+\\((?P<player2>[a-zA-Z-\\\'\\s\\.]+)\\s+draws\\s+the\\s+foul\\)','<player> personal foul (<player2> draws the foul)',0,0,0,11,1,0,1,0,1,0,0,0,0),(42,'<b>(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+makes\\s+free\\s+throw\\s+1\\s+of\\s+2</b>','<b><player> makes free throw 1 of 2</b>',0,1,1,1,0,0,1,0,0,0,0,0,0),(43,'<b>(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+makes\\s+free\\s+throw\\s+2\\s+of\\s+2</b>','<b><player> makes free throw 2 of 2</b>',0,1,1,1,0,0,1,0,0,0,0,0,0),(44,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+misses\\s+(?P<distance>[0-9]{1,2})-foot\\s+three\\s+point\\s+jumper','<player> misses <distance>-foot three point jumper',1,0,0,2,0,0,1,0,0,0,0,3,0),(45,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+personal\\s+foul\\s+\\((?P<player2>[a-zA-Z-\\\'\\s\\.]+)\\s+draws\\s+the\\s+foul\\)','<player> personal foul (<player2> draws the foul)',0,0,0,11,1,0,1,0,1,0,0,0,0),(46,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+offensive\\s+rebound','<player> offensive rebound',0,0,0,4,0,0,1,1,0,0,0,0,0),(47,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+misses\\s+(?P<distance>[0-9]{1,2})-foot\\s+jumper','<player> misses <distance>-foot jumper',1,0,0,11,0,0,1,0,0,0,0,2,0),(48,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+enters\\s+the\\s+game\\s+for\\s+(?P<player2>[a-zA-Z-\\\'\\s\\.]+)','<player> enters the game for <player2>',0,0,0,1,1,0,1,0,0,0,0,0,0),(49,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+defensive\\s+rebound','<player> defensive rebound',0,0,0,4,0,0,1,1,0,0,0,0,0),(50,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+misses\\s+two\\s+point\\s+shot','<player> misses two point shot',1,0,0,1,0,0,1,0,0,0,0,2,0),(51,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+kicked\\s+ball','<player> kicked ball',0,0,0,4,0,0,1,0,0,0,0,0,0),(52,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+double\\s+dribble','<player> double dribble',0,0,0,4,0,0,1,0,0,1,0,0,0),(53,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+offensive\\s+goaltending','<player> offensive goaltending',0,0,0,11,0,0,1,0,0,0,0,0,0),(54,'<b>(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+makes\\s+free\\s+throw\\s+1\\s+of\\s+3</b>','<b><player> makes free throw 1 of 3</b>',0,1,1,1,0,0,1,0,0,0,0,0,0),(55,'<b>(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+makes\\s+free\\s+throw\\s+2\\s+of\\s+3</b>','<b><player> makes free throw 2 of 3</b>',0,1,1,1,0,0,1,0,0,0,0,0,0),(56,'<b>(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+makes\\s+free\\s+throw\\s+3\\s+of\\s+3</b>','<b><player> makes free throw 3 of 3</b>',0,1,1,1,0,0,1,0,0,0,0,0,0),(57,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+misses\\s+free\\s+throw\\s+1\\s+of\\s+3','<player> misses free throw 1 of 3',0,1,0,1,0,0,1,0,0,0,0,0,0),(58,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+misses\\s+free\\s+throw\\s+2\\s+of\\s+3','<player> misses free throw 2 of 3',0,1,0,1,0,0,1,0,0,0,0,0,0),(59,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+misses\\s+free\\s+throw\\s+3\\s+of\\s+3','<player> misses free throw 3 of 3',0,1,0,1,0,0,1,0,0,0,0,0,0),(60,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+3\\s+second','<player> 3 second',0,0,0,4,0,0,1,0,0,0,0,0,0),(61,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+lane\\s+violation','<player> lane violation',0,0,0,4,0,0,1,0,0,0,0,0,0),(62,'8\\s+second','8 second',0,0,0,4,0,0,1,0,0,1,0,0,0),(63,'turnover','turnover',0,0,0,4,0,0,1,0,0,1,0,0,0),(65,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+offensive\\s+charge\\s+\\((?P<player2>[a-zA-Z-\\\'\\s\\.]+)\\s+draws\\s+the\\s+foul\\)','<player> offensive charge (<player2> draws the foul)',0,0,0,11,1,0,1,0,1,0,0,0,0),(70,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+personal\\s+block\\s+\\((?P<player2>[a-zA-Z-\\\'\\s\\.]+)\\s+draws\\s+the\\s+foul\\)','<player> personal block (<player2> draws the foul)',0,0,0,11,1,0,1,0,1,0,0,0,0),(69,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+personal\\s+take\\s+\\((?P<player2>[a-zA-Z-\\\'\\s\\.]+)\\s+draws\\s+the\\s+foul\\)','<player> personal take (<player2> draws the foul)',0,0,0,11,1,0,1,0,1,0,0,0,0),(71,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+illegal\\s+defense\\s+foul','<player> illegal defense foul',0,0,0,6,0,0,1,0,1,0,0,0,0),(72,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+double\\s+technical\\s+foul','<player> double technical foul',0,0,0,6,0,0,0,0,1,0,0,0,0),(73,'backcourt','backcourt',0,0,0,4,0,0,1,0,0,1,0,0,0),(74,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+double\\s+personal\\s+foul','<player> double personal foul',0,0,0,6,0,0,1,0,1,0,0,0,0),(75,'double\\s+personal\\s+foul:\\s+(?P<player1>[a-zA-Z-\\\'\\s\\.]+)\\s+\\(([0-9])\\)\\s+and\\s+(?P<player2>[a-zA-Z-\\\'\\s\\.]+)\\s+\\(([0-9])\\)\\s+are\\s+each\\s+charged\\s+with\\s+a\\s+personal\\s+foul','double personal foul: <player1> and <player2> are each charged with a personal foul',0,0,0,6,1,1,1,0,1,0,0,0,0),(76,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+discontinue\\s+dribble','<player> discontinue dribble',0,0,0,4,0,0,1,0,0,0,0,0,0),(77,'<b>(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+makes\\s+flagrant\\s+free\\s+throw\\s+1\\s+of\\s+2</b>','<b><player> makes flagrant free throw 1 of 2</b>',0,1,1,1,0,0,1,0,0,0,0,0,0),(78,'<b>(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+makes\\s+flagrant\\s+free\\s+throw\\s+2\\s+of\\s+2</b>','<b><player> makes flagrant free throw 2 of 2</b>',0,1,1,1,0,0,1,0,0,0,0,0,0),(79,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+misses\\s+flagrant\\s+free\\s+throw\\s+1\\s+of\\s+2','<player> misses flagrant free throw 1 of 2',0,1,0,1,0,0,1,0,0,0,0,0,0),(80,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+misses\\s+flagrant\\s+free\\s+throw\\s+2\\s+of\\s+2','<player> misses flagrant free throw 2 of 2',0,1,0,1,0,0,1,0,0,0,0,0,0),(81,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+flagrant\\s+foul\\s+type\\s+1\\s+\\((?P<player2>[a-zA-Z-\\\'\\s\\.]+)\\s+draws\\s+the\\s+foul\\)','<player> flagrant foul type 1 (<player2> draws the foul)',0,0,0,6,1,0,1,0,1,0,0,0,0),(82,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+ejected','<player> ejected',0,0,0,4,0,0,0,0,0,0,0,0,0),(83,'Double\\s+technical\\s+foul:\\s+(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+and\\s+(?P<player2>[a-zA-Z-\\\'\\s\\.]+)','Double technical foul: <player1> and <player2>',0,0,0,6,1,1,1,0,1,0,0,0,0),(84,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+lost\\s+ball','<player> lost ball',0,0,0,4,0,0,1,0,0,1,0,0,0),(85,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+jump\\s+ball','<player> jump ball',0,0,0,4,0,0,1,0,0,0,0,0,0),(86,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+jump\\s+ball\\s+violation','<player> jump ball violation',0,0,0,4,0,0,1,0,0,0,0,0,0),(87,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+inbound','<player> inbound',0,0,0,4,0,0,1,0,0,0,0,0,0),(88,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+flagrant\\s+foul\\s+type\\s+2\\s+\\((?P<player2>[a-zA-Z-\\\'\\s\\.]+)\\s+draws\\s+the\\s+foul\\)','<player> flagrant foul type 2 (<player2> draws the foul)',0,0,0,6,1,0,1,0,1,0,0,0,0),(89,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+taunting\\s+technical\\s+\\((\\d)(st|nd|rd|th)\\s+personal\\s+foul\\)','<player> taunting technical',0,0,0,6,0,0,0,0,0,0,0,0,0),(90,'','unknown play',0,0,0,101,0,0,1,0,0,0,0,0,0),(0,'','play not identified',0,0,0,101,0,0,1,0,0,0,0,0,0),(95,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+defensive\\s+goaltending','<player> defensive goaltending',0,0,0,11,0,0,1,0,0,0,0,0,0),(93,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+(?P<foul_type>(shooting|offensive|personal|loose\\sball|clear\\spath|technical|hanging\\son\\srim))\\s+foul\\s+\\((?P<foul_info>[0-9a-zA-Z-\\\'\\s\\.]+)\\)','<player> <foul_type> foul (<foul_info>)',0,0,0,10,0,0,0,0,1,0,0,0,0),(94,'(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+foul\\s+\\((?P<player2>[a-zA-Z-\\\'\\s\\.]+)\\s+draws\\s+the\\s+foul\\)','<player> foul (<player2> draws the foul)',0,0,0,6,1,0,1,0,1,0,0,0,0),(96,'<b>(?P<player>[a-zA-Z-\\\'\\s\\.]+)\\s+makes\\s+(?P<distance>[0-9]{1,2})-foot\\s+three\\s+point\\s+jumper</b>','<b><player> makes <distance>-foot three point jumper</b>',NULL,NULL,0,2,NULL,NULL,NULL,0,0,0,0,NULL,NULL);
/*!40000 ALTER TABLE `play_espn` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-03-27  9:09:57
