-- MySQL dump 10.13  Distrib 5.1.58, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: nba
-- ------------------------------------------------------
-- Server version	5.1.58-1ubuntu1

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
-- Table structure for table `boxscore`
--

DROP TABLE IF EXISTS `boxscore`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boxscore` (
  `game_id` int(11) DEFAULT NULL,
  `player_id` int(11) DEFAULT NULL,
  `team_code` varchar(10) DEFAULT NULL,
  `fgm` tinyint(4) DEFAULT NULL,
  `fga` tinyint(4) DEFAULT NULL,
  `3ptm` tinyint(4) DEFAULT NULL,
  `3pta` tinyint(4) DEFAULT NULL,
  `ftm` tinyint(4) DEFAULT NULL,
  `fta` tinyint(4) DEFAULT NULL,
  `points` tinyint(4) DEFAULT NULL,
  KEY `idx_game_id` (`game_id`),
  KEY `idx_player_id` (`player_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cbsshot`
--

DROP TABLE IF EXISTS `cbsshot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cbsshot` (
  `id` int(11) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `is_freethrow` tinyint(4) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `combined`
--

DROP TABLE IF EXISTS `combined`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `combined` (
  `playbyplay_id` int(11) DEFAULT NULL,
  `game_id` int(11) DEFAULT NULL,
  `period` int(11) DEFAULT NULL,
  `play_num` int(11) DEFAULT NULL,
  `sec_elapsed_game` int(11) DEFAULT NULL,
  `away_score` int(11) DEFAULT NULL,
  `home_score` int(11) DEFAULT NULL,
  `play_id` int(11) DEFAULT NULL,
  `team_code` varchar(10) DEFAULT NULL,
  `player_id` int(11) DEFAULT NULL,
  `player1_id` int(11) DEFAULT NULL,
  `player2_id` int(11) DEFAULT NULL,
  `assist_player_id` int(11) DEFAULT NULL,
  `foul_type` varchar(50) DEFAULT NULL,
  `foul_info` varchar(50) DEFAULT NULL,
  `shot_type` varchar(50) DEFAULT NULL,
  `distance` int(11) DEFAULT NULL,
  `away_fiveman` varchar(30) DEFAULT NULL,
  `home_fiveman` varchar(30) DEFAULT NULL,
  `away_play_desc` varchar(500) DEFAULT NULL,
  `home_play_desc` varchar(500) DEFAULT NULL,
  `play_desc` varchar(500) DEFAULT NULL,
  `shot_num_shotchart` int(11) DEFAULT NULL,
  `x` int(11) DEFAULT NULL,
  `y` int(11) DEFAULT NULL,
  `distance_shotchart` int(11) DEFAULT NULL,
  `cbs_shot_type_id` int(11) DEFAULT NULL,
  `sec_elapsed_game_shotchart` int(11) DEFAULT NULL,
  KEY `idx_player_id` (`player_id`),
  KEY `idx_player1_id` (`player1_id`),
  KEY `idx_assist_player_id` (`assist_player_id`),
  KEY `idx_play_id` (`play_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dim_times`
--

DROP TABLE IF EXISTS `dim_times`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dim_times` (
  `sec_elapsed_game` int(11) DEFAULT NULL,
  `sec_elapsed_period` int(11) DEFAULT NULL,
  `sec_left_period` int(11) DEFAULT NULL,
  `time_left` varchar(10) DEFAULT NULL,
  `period` int(11) DEFAULT NULL,
  `period_name` varchar(20) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `extract_ref`
--

DROP TABLE IF EXISTS `extract_ref`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `extract_ref` (
  `game_id` int(11) DEFAULT NULL,
  `period_name` varchar(20) DEFAULT NULL,
  `play_num` int(11) DEFAULT NULL,
  `time_left` varchar(10) DEFAULT NULL,
  `away_score` tinyint(4) DEFAULT NULL,
  `home_score` tinyint(4) DEFAULT NULL,
  `away_play` varchar(200) DEFAULT NULL,
  `home_play` varchar(200) DEFAULT NULL,
  `sec_elapsed_game` int(11) DEFAULT NULL,
  KEY `idx_game_id_play_num` (`game_id`,`play_num`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `game`
--

DROP TABLE IF EXISTS `game`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `game` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `away_team` varchar(3) DEFAULT NULL,
  `home_team` varchar(3) DEFAULT NULL,
  `date_played` date NOT NULL,
  `abbrev` varchar(20) NOT NULL,
  `espn_game_id` int(11) DEFAULT NULL,
  `cbssports_game_id` varchar(20) DEFAULT NULL,
  `nbacom_game_id` varchar(15) DEFAULT NULL,
  `gametime` varchar(20) DEFAULT NULL,
  `national_tv` varchar(20) DEFAULT NULL,
  `season` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_abbrev` (`abbrev`)
) ENGINE=MyISAM AUTO_INCREMENT=2256 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pbp2`
--

DROP TABLE IF EXISTS `pbp2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pbp2` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) DEFAULT NULL,
  `period` int(11) DEFAULT NULL,
  `play_num` int(11) DEFAULT NULL,
  `sec_elapsed_game` int(11) DEFAULT NULL,
  `away_score` int(11) DEFAULT NULL,
  `home_score` int(11) DEFAULT NULL,
  `play_id` int(11) DEFAULT NULL,
  `team_code` varchar(10) DEFAULT NULL,
  `player_id` int(11) DEFAULT '0',
  `player1_id` int(11) DEFAULT '0',
  `player2_id` int(11) DEFAULT '0',
  `assist_player_id` int(11) DEFAULT '0',
  `foul_type` varchar(50) DEFAULT NULL,
  `foul_info` varchar(50) DEFAULT NULL,
  `shot_type` varchar(50) DEFAULT NULL,
  `distance` int(11) DEFAULT NULL,
  `away_fiveman` varchar(30) DEFAULT NULL,
  `home_fiveman` varchar(30) DEFAULT NULL,
  `away_play_desc` varchar(500) DEFAULT NULL,
  `home_play_desc` varchar(500) DEFAULT NULL,
  `play_desc` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_play_num` (`play_num`),
  KEY `idx_game_id` (`game_id`)
) ENGINE=MyISAM AUTO_INCREMENT=373524 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pbpidx`
--

DROP TABLE IF EXISTS `pbpidx`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pbpidx` (
  `game_id` int(11) DEFAULT NULL,
  `period` int(11) DEFAULT NULL,
  `play_num` int(11) DEFAULT NULL,
  `sec_elapsed_game` int(11) DEFAULT NULL,
  `away_score` int(11) DEFAULT NULL,
  `home_score` int(11) DEFAULT NULL,
  `play_id` int(11) DEFAULT NULL,
  `team_code` varchar(10) DEFAULT NULL,
  `player_id` int(11) DEFAULT NULL,
  `player1_id` int(11) DEFAULT NULL,
  `player2_id` int(11) DEFAULT NULL,
  `assist_player_id` int(11) DEFAULT NULL,
  `foul_type` varchar(50) DEFAULT NULL,
  `foul_info` varchar(50) DEFAULT NULL,
  `shot_type` varchar(50) DEFAULT NULL,
  `distance` int(11) DEFAULT NULL,
  KEY `idx_game_id` (`game_id`),
  KEY `idx_play_num` (`play_num`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pbptest`
--

DROP TABLE IF EXISTS `pbptest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pbptest` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) DEFAULT NULL,
  `period` int(11) DEFAULT NULL,
  `play_num` int(11) DEFAULT NULL,
  `sec_elapsed_game` int(11) DEFAULT NULL,
  `away_score` int(11) DEFAULT NULL,
  `home_score` int(11) DEFAULT NULL,
  `play_id` int(11) DEFAULT NULL,
  `team_code` varchar(10) DEFAULT NULL,
  `player_id` int(11) DEFAULT NULL,
  `player1_id` int(11) DEFAULT NULL,
  `player2_id` int(11) DEFAULT NULL,
  `assist_player_id` int(11) DEFAULT NULL,
  `foul_type` varchar(50) DEFAULT NULL,
  `foul_info` varchar(50) DEFAULT NULL,
  `shot_type` varchar(50) DEFAULT NULL,
  `distance` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_play_num` (`play_num`),
  KEY `idx_game_id` (`game_id`)
) ENGINE=MyISAM AUTO_INCREMENT=383724 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pbptestwithid`
--

DROP TABLE IF EXISTS `pbptestwithid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pbptestwithid` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) DEFAULT NULL,
  `period` int(11) DEFAULT NULL,
  `play_num` int(11) DEFAULT NULL,
  `sec_elapsed_game` int(11) DEFAULT NULL,
  `away_score` int(11) DEFAULT NULL,
  `home_score` int(11) DEFAULT NULL,
  `play_id` int(11) DEFAULT NULL,
  `team_code` varchar(10) DEFAULT NULL,
  `player_id` int(11) DEFAULT NULL,
  `player1_id` int(11) DEFAULT NULL,
  `player2_id` int(11) DEFAULT NULL,
  `assist_player_id` int(11) DEFAULT NULL,
  `foul_type` varchar(50) DEFAULT NULL,
  `foul_info` varchar(50) DEFAULT NULL,
  `shot_type` varchar(50) DEFAULT NULL,
  `distance` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=381484 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `play`
--

DROP TABLE IF EXISTS `play`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `play` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `re` varchar(1000) NOT NULL,
  `name` varchar(1000) NOT NULL,
  `is_shot` tinyint(1) DEFAULT NULL,
  `is_freethrow` tinyint(4) DEFAULT NULL,
  `is_shot_made` tinyint(4) NOT NULL DEFAULT '0',
  `priority` smallint(6) DEFAULT NULL,
  `has_player2` tinyint(4) DEFAULT NULL,
  `has_player1` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=96 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `play_nbacom`
--

DROP TABLE IF EXISTS `play_nbacom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `play_nbacom` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nbacom_id` int(11) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `shot_group` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=65 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `player`
--

DROP TABLE IF EXISTS `player`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `player` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) DEFAULT NULL,
  `alternate_name` varchar(100) DEFAULT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `cbssports_player_id` int(11) DEFAULT NULL,
  `espn_player_id` int(11) DEFAULT NULL,
  `team_code` varchar(10) DEFAULT NULL,
  `jersey` varchar(10) DEFAULT NULL,
  `position` varchar(30) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `is_current` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=968 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `playerbk`
--

DROP TABLE IF EXISTS `playerbk`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `playerbk` (
  `id` int(11) NOT NULL DEFAULT '0',
  `full_name` varchar(100) DEFAULT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `cbssports_player_id` int(11) DEFAULT NULL,
  `espn_player_id` int(11) DEFAULT NULL,
  `team_code` varchar(10) DEFAULT NULL,
  `jersey` varchar(10) DEFAULT NULL,
  `position` varchar(30) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `is_current` tinyint(1) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shot2`
--

DROP TABLE IF EXISTS `shot2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shot2` (
  `game_id` int(11) DEFAULT NULL,
  `shot_num` int(11) DEFAULT NULL,
  `team_code` varchar(10) DEFAULT NULL,
  `sec_elapsed_game` int(11) DEFAULT NULL,
  `period` int(11) DEFAULT NULL,
  `player_id` int(11) DEFAULT NULL,
  `shot_type_id` int(11) DEFAULT NULL,
  `result` int(11) DEFAULT NULL,
  `x` int(11) DEFAULT NULL,
  `y` int(11) DEFAULT NULL,
  `distance` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shottest`
--

DROP TABLE IF EXISTS `shottest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shottest` (
  `game_id` int(11) DEFAULT NULL,
  `shot_num` int(11) DEFAULT NULL,
  `team_code` varchar(10) DEFAULT NULL,
  `sec_elapsed_game` int(11) DEFAULT NULL,
  `period` int(11) DEFAULT NULL,
  `player_id` int(11) DEFAULT NULL,
  `shot_type_id` int(11) DEFAULT NULL,
  `result` int(11) DEFAULT NULL,
  `x` int(11) DEFAULT NULL,
  `y` int(11) DEFAULT NULL,
  `distance` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shottestbk`
--

DROP TABLE IF EXISTS `shottestbk`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shottestbk` (
  `game_id` int(11) DEFAULT NULL,
  `shot_num` int(11) DEFAULT NULL,
  `team_code` varchar(10) DEFAULT NULL,
  `sec_elapsed_game` int(11) DEFAULT NULL,
  `period` int(11) DEFAULT NULL,
  `player_id` int(11) DEFAULT NULL,
  `shot_type_id` int(11) DEFAULT NULL,
  `result` int(11) DEFAULT NULL,
  `x` int(11) DEFAULT NULL,
  `y` int(11) DEFAULT NULL,
  `distance` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `team`
--

DROP TABLE IF EXISTS `team`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `team` (
  `code` varchar(3) NOT NULL DEFAULT '',
  `name` varchar(30) NOT NULL,
  `city` varchar(30) NOT NULL,
  `nickname` varchar(30) NOT NULL,
  `alternate_nickname` varchar(30) NOT NULL,
  `nbacom_code` char(3) DEFAULT NULL,
  PRIMARY KEY (`code`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `test`
--

DROP TABLE IF EXISTS `test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `test` (
  `id` int(11) DEFAULT NULL,
  `val` varchar(10) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2011-12-21 18:48:17
