-- MySQL dump 10.13  Distrib 5.5.23, for osx10.6 (i386)
--
-- Host: localhost    Database: nba
-- ------------------------------------------------------
-- Server version	5.5.23

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
-- Table structure for table `play_type_nbacom`
--

DROP TABLE IF EXISTS `play_type_nbacom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `play_type_nbacom` (
  `id` int(11) NOT NULL,
  `re` varchar(500) DEFAULT NULL,
  `name` varchar(200) DEFAULT NULL,
  `is_rebound` tinyint(4) DEFAULT NULL,
  `is_freethrow` tinyint(4) DEFAULT NULL,
  `is_shot` tinyint(4) DEFAULT NULL,
  `is_shot_made` tinyint(4) DEFAULT NULL,
  `is_turnover` tinyint(4) DEFAULT NULL,
  `is_foul` tinyint(4) DEFAULT '0',
  `is_period_startend` tinyint(4) DEFAULT NULL,
  `is_team_play` tinyint(4) DEFAULT '0',
  `is_timeout` tinyint(4) DEFAULT '0',
  `is_freethrow_made` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `play_type_nbacom`
--

LOCK TABLES `play_type_nbacom` WRITE;
/*!40000 ALTER TABLE `play_type_nbacom` DISABLE KEYS */;
INSERT INTO `play_type_nbacom` VALUES (0,'fake\\s+pattern',NULL,0,0,0,0,0,0,0,0,0,0),(1,'(&lt;\\!\\[CDATA\\[)*\\(\\d{2}:\\d{2}(\\.\\d)*\\)\\s*End\\s+Period(\\]\\]&gt;)*',NULL,0,0,0,0,0,0,1,0,0,0),(2,'(&lt;\\!\\[CDATA\\[)*\\(\\d{2}:\\d{2}(\\.\\d)*\\)\\s*Start\\s+Period(\\]\\]&gt;)*',NULL,0,0,0,0,0,0,1,0,0,0),(3,'(&lt;\\!\\[CDATA\\[)*\\(\\d{2}:\\d{2}(\\.\\d)*\\)\\[[a-zA-Z]{2,3}\\]\\s+Team\\s+Rebound(\\]\\]&gt;)*',NULL,1,0,0,0,0,0,0,1,0,0),(4,'(&lt;\\!\\[CDATA\\[)*\\(\\d{2}:\\d{2}(\\.\\d)*\\)\\[[a-zA-Z]{2,3}\\]\\s+Team\\s+Timeout\\s+:\\s+(Regular|Short)(\\]\\]&gt;)*',NULL,0,0,0,0,0,0,0,0,1,0),(5,'(&lt;\\!\\[CDATA\\[)*\\(\\d{2}:\\d{2}(\\.\\d)*\\)\\s*Timeout\\s+:\\s+(Official|Regular)(\\]\\]&gt;)*',NULL,0,0,0,0,0,0,0,0,1,0),(6,'(&lt;\\!\\[CDATA\\[)*\\(\\d{2}:\\d{2}(\\.\\d)*\\)\\[[a-zA-Z]{2,3}\\]\\s+(?P<player_id>[a-zA-Z-\\s]+)\\s+Rebound\\s+\\(Off:\\d+\\s+Def:\\d+\\)(\\]\\]&gt;)*',NULL,1,0,0,0,0,0,0,0,0,0),(7,'(&lt;\\!\\[CDATA\\[)*\\(\\d{2}:\\d{2}(\\.\\d)*\\)\\[[a-zA-Z]{2,3}\\]\\s+(?P<player_id>[a-zA-Z-\\s]+)\\s+(?P<shot_type>(3pt|Jump|Tip|Layup|Jump Hook|Turnaround Jump|Putback Dunk|Dunk|Pullup Jump|Jump Bank|Running Bank|Running Bank Hook|Hook|Turnaround Fadeaway))\\s+(s|S)hot:\\s+Missed(\\]\\]&gt;)*',NULL,0,0,1,0,0,0,0,0,0,0),(8,'(&lt;\\!\\[CDATA\\[)*\\(\\d{2}:\\d{2}(\\.\\d)*\\)\\[[a-zA-Z]{2,3}\\]\\s+(?P<player_id>[a-zA-Z-\\s]+)\\s+(?P<shot_type>(3pt|Jump|Tip|Layup|Jump Hook|Turnaround Jump|Putback Dunk|Dunk|Pullup Jump|Jump Bank|Running Bank|Running Bank Hook|Hook|Turnaround Fadeaway))\\s+(s|S)hot:\\s+Missed\\s+Block:\\s*(?P<player2_id>[a-zA-Z-\\s]+)\\s*\\(\\d+\\s+BLK\\)(\\]\\]&gt;)*',NULL,0,0,1,0,0,0,0,0,0,0),(9,'(&lt;\\!\\[CDATA\\[)*\\(\\d{2}:\\d{2}(\\.\\d)*\\)\\[[a-zA-Z]{2,3}\\]\\s+(?P<player_id>[a-zA-Z-\\s]+)\\s+Free\\s+Throw\\s+(Flagrant|Technical)*\\s*(?P<ft_count>\\d)\\s+of\\s+(?P<ft_total>\\d)\\s+Missed(\\]\\]&gt;)*',NULL,0,1,0,0,0,0,0,0,0,0),(10,'(&lt;\\!\\[CDATA\\[)*\\(\\d{2}:\\d{2}(\\.\\d)*\\)\\[[a-zA-Z]{2,3}\\s+\\d+\\-\\d+\\]\\s+(?P<player_id>[a-zA-Z-\\s]+)\\s+Free\\s+Throw\\s+(Flagrant|Technical)*\\s*(?P<ft_count>\\d)\\s+of\\s+(?P<ft_total>\\d)\\s+\\(\\d+\\s+PTS\\)(\\]\\]&gt;)*',NULL,0,1,0,1,0,0,0,0,0,1),(11,'(&lt;\\!\\[CDATA\\[)*\\(\\d{2}:\\d{2}(\\.\\d)*\\)\\[[a-zA-Z]{2,3}\\s+\\d+\\-\\d+\\]\\s+(?P<player_id>[a-zA-Z-\\s]+)\\s+Free\\s+Throw\\s+(Flagrant|Technical)*\\s*\\(\\d+\\s+PTS\\)(\\]\\]&gt;)*',NULL,0,1,0,1,0,0,0,0,0,1),(12,'(&lt;\\!\\[CDATA\\[)*\\(\\d{2}:\\d{2}(\\.\\d)*\\)\\[[a-zA-Z]{2,3}\\]\\s+(?P<player2_id>[a-zA-Z-\\s]+)\\s+Substitution\\s+replaced\\s+by\\s+(?P<player_id>[a-zA-Z-\\s]+)(\\]\\]&gt;)*',NULL,0,0,0,0,0,0,0,0,0,0),(13,'(&lt;\\!\\[CDATA\\[)*\\(\\d{2}:\\d{2}(\\.\\d)*\\)\\[[a-zA-Z]{2,3}\\s+\\d+\\-\\d+\\]\\s+(?P<player_id>[a-zA-Z-\\s]+)\\s+(?P<shot_type>(3pt|Jump|Tip|Layup|Jump Hook|Turnaround Jump|Putback Dunk|Dunk|Pullup Jump|Jump Bank|Running Bank|Running Bank Hook|Hook|Turnaround Fadeaway))\\s+(s|S)hot:\\s+Made\\s+\\(\\d+\\s+PTS\\)(\\]\\]&gt;)*',NULL,0,0,1,1,0,0,0,0,0,0),(14,'(&lt;\\!\\[CDATA\\[)*\\(\\d{2}:\\d{2}(\\.\\d)*\\)\\[[a-zA-Z]{2,3}\\s+\\d+\\-\\d+\\]\\s+(?P<player_id>[a-zA-Z-\\s]+)\\s+(?P<shot_type>(3pt|Jump|Tip|Layup|Jump Hook|Turnaround Jump|Putback Dunk|Dunk|Pullup Jump|Jump Bank|Running Bank|Running Bank Hook|Hook|Turnaround Fadeaway))\\s+(s|S)hot:\\s+Made\\s+\\(\\d+\\s+PTS\\)\\s+Assist:\\s+(?P<player2_id>[a-zA-Z-\\s]+)\\s+\\(\\d+\\s+AST\\)(\\]\\]&gt;)*',NULL,0,0,1,1,0,0,0,0,0,0),(15,'(&lt;\\!\\[CDATA\\[)*\\(\\d{2}:\\d{2}(\\.\\d)*\\)\\[[a-zA-Z]{2,3}\\]\\s+(?P<player_id>[a-zA-Z-\\s]+)\\s+Foul:\\s+(Shooting|Personal|Loose Ball|Offensive|Personal Block|Personal Take|Offensive Charge|Flagrant Type \\d)\\s+\\(\\d+\\s+PF\\)(\\]\\]&gt;)*',NULL,0,0,0,0,0,1,0,0,0,0),(16,'(&lt;\\!\\[CDATA\\[)*\\(\\d{2}:\\d{2}(\\.\\d)*\\)\\[[a-zA-Z]{2,3}\\]\\s+(?P<player_id>[a-zA-Z-\\s]+)\\s+Turnover\\s+:\\s+(Bad Pass|Traveling|Lost Ball|Foul|Step Out of Bounds Turnover|Out of Bounds Lost Ball Turnover|Poss Lost Ball Turnover)\\s+\\(\\d+\\s+TO\\)(\\]\\]&gt;)*',NULL,0,0,0,0,1,0,0,0,0,0),(17,'(&lt;\\!\\[CDATA\\[)*\\(\\d{2}:\\d{2}(\\.\\d)*\\)\\[[a-zA-Z]{2,3}\\]\\s+(?P<player_id>[a-zA-Z-\\s]+)\\s+Turnover\\s+:\\s+(Bad Pass|Traveling|Lost Ball|Foul|Step Out of Bounds Turnover|Out of Bounds Lost Ball Turnover|Poss Lost Ball Turnover)\\s+\\(\\d+\\s+TO\\)\\s+Steal\\s*:\\s*(?P<player2_id>[a-zA-Z-\\s]+)\\s+\\(\\d+\\s+ST\\)(\\]\\]&gt;)*',NULL,0,0,0,0,0,0,0,0,0,0),(18,'(&lt;\\!\\[CDATA\\[)*\\(\\d{2}:\\d{2}(\\.\\d)*\\)\\s*Jump\\s+Ball\\s+(?P<player1_id>[a-zA-Z-\\s]+)\\s+vs\\s+(?P<player2_id>[a-zA-Z-\\s]+)\\s+\\((?P<player_id>[a-zA-Z-\\s]+)\\s+gains\\s+possession\\)(\\]\\]&gt;)*',NULL,0,0,0,0,0,0,0,0,0,0),(19,'(&lt;\\!\\[CDATA\\[)*\\(\\d{2}:\\d{2}(\\.\\d)*\\)\\[[a-zA-Z]{2,3}\\]\\s+(?P<player_id>[a-zA-Z-\\s]+)\\s+Violation:\\s*(Defensive Goaltending|Kicked Ball)(\\]\\]&gt;)*',NULL,0,0,0,0,0,0,0,0,0,0),(20,'(&lt;\\!\\[CDATA\\[)*\\(\\d{2}:\\d{2}(\\.\\d)*\\)\\[[a-zA-Z]{2,3}\\]\\s+(?P<player_id>[a-zA-Z-\\s]+)\\s+Technical(\\]\\]&gt;)*',NULL,0,0,0,0,0,1,0,0,0,0);
/*!40000 ALTER TABLE `play_type_nbacom` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-11-03 16:16:35
