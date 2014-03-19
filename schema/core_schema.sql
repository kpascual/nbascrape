
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
DROP TABLE IF EXISTS `boxscore_nbacom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boxscore_nbacom` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) DEFAULT NULL,
  `player_id` int(11) DEFAULT NULL,
  `team_id` int(11) DEFAULT NULL,
  `is_dnp` tinyint(4) DEFAULT NULL,
  `time_played` varchar(10) DEFAULT NULL,
  `sec_played` int(11) DEFAULT NULL,
  `fgm` tinyint(4) DEFAULT NULL,
  `fga` tinyint(4) DEFAULT NULL,
  `threeptm` tinyint(4) DEFAULT NULL,
  `threepta` tinyint(4) DEFAULT NULL,
  `ftm` tinyint(4) DEFAULT NULL,
  `fta` tinyint(4) DEFAULT NULL,
  `off_reb` tinyint(4) DEFAULT NULL,
  `def_reb` tinyint(4) DEFAULT NULL,
  `total_reb` tinyint(4) DEFAULT NULL,
  `assists` tinyint(4) DEFAULT NULL,
  `personal_fouls` tinyint(4) DEFAULT NULL,
  `steals` tinyint(4) DEFAULT NULL,
  `turnovers` tinyint(4) DEFAULT NULL,
  `blocks` tinyint(4) DEFAULT NULL,
  `blocks_against` tinyint(4) DEFAULT NULL,
  `plusminus` varchar(5) DEFAULT NULL,
  `total_points` tinyint(4) DEFAULT NULL,
  `unknown12` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_game_player` (`game_id`,`player_id`),
  KEY `idx_game_id` (`game_id`),
  KEY `idx_player_id` (`player_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `boxscore_cbssports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boxscore_cbssports` (
  `game_id` int(11) DEFAULT NULL,
  `player_id` int(11) DEFAULT NULL,
  `team_id` int(11) DEFAULT NULL,
  `fgm` tinyint(4) DEFAULT NULL,
  `fga` tinyint(4) DEFAULT NULL,
  `3ptm` tinyint(4) DEFAULT NULL,
  `3pta` tinyint(4) DEFAULT NULL,
  `ftm` tinyint(4) DEFAULT NULL,
  `fta` tinyint(4) DEFAULT NULL,
  `points` tinyint(4) DEFAULT NULL,
  UNIQUE KEY `idx_game_player` (`game_id`,`player_id`),
  KEY `idx_game_id` (`game_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `shotchart_nbacom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shotchart_nbacom` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) DEFAULT NULL,
  `nbacom_play_num` int(11) DEFAULT NULL,
  `player_id` int(11) DEFAULT NULL,
  `x` int(11) DEFAULT NULL,
  `y` int(11) DEFAULT NULL,
  `shot_type_nbacom_id` int(11) DEFAULT NULL,
  `period` tinyint(4) DEFAULT NULL,
  `deciseconds_left` int(11) DEFAULT NULL,
  `team_id` int(11) DEFAULT NULL,
  `is_shot_made` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_game_play` (`game_id`,`nbacom_play_num`),
  KEY `idx_game_id` (`game_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `shotchart_espn`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shotchart_espn` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) DEFAULT NULL,
  `espn_play_num` bigint(20) DEFAULT NULL,
  `player_id` int(11) DEFAULT NULL,
  `x` int(11) DEFAULT NULL,
  `y` int(11) DEFAULT NULL,
  `shot_type` varchar(50) DEFAULT NULL,
  `period` tinyint(4) DEFAULT NULL,
  `deciseconds_left` int(11) DEFAULT NULL,
  `team_id` int(11) DEFAULT NULL,
  `distance` int(11) DEFAULT NULL,
  `is_shot_made` tinyint(4) DEFAULT NULL,
  `shot_desc` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_game_play` (`game_id`,`espn_play_num`),
  KEY `idx_game_id` (`game_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `shotchart_cbssports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shotchart_cbssports` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) DEFAULT NULL,
  `shot_num` int(11) DEFAULT NULL,
  `team_id` int(11) DEFAULT NULL,
  `deciseconds_left` int(11) DEFAULT NULL,
  `period` int(11) DEFAULT NULL,
  `player_id` int(11) DEFAULT NULL,
  `shot_type_cbssports_id` int(11) DEFAULT NULL,
  `is_shot_made` tinyint(4) DEFAULT NULL,
  `x` int(11) DEFAULT NULL,
  `y` int(11) DEFAULT NULL,
  `distance` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_game_shot` (`game_id`,`shot_num`),
  KEY `idx_game_id` (`game_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `playbyplay_nbacom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `playbyplay_nbacom` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) DEFAULT NULL,
  `player_id` int(11) DEFAULT NULL,
  `team_id` int(11) DEFAULT NULL,
  `period` int(11) DEFAULT NULL,
  `deciseconds_left` int(11) DEFAULT NULL,
  `player2_id` int(11) DEFAULT NULL,
  `player1_id` int(11) DEFAULT NULL,
  `play_index` int(11) DEFAULT NULL,
  `msg_type` smallint(6) DEFAULT NULL,
  `play_desc` varchar(500) DEFAULT NULL,
  `ft_count` tinyint(4) DEFAULT NULL,
  `ft_total` tinyint(4) DEFAULT NULL,
  `shot_type` varchar(50) DEFAULT NULL,
  `away_score` smallint(6) DEFAULT NULL,
  `home_score` smallint(6) DEFAULT NULL,
  `action_type` smallint(6) DEFAULT NULL,
  `play_type_nbacom_id` int(11) DEFAULT NULL,
  `info` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_game_event` (`game_id`,`play_index`),
  KEY `idx_game_id` (`game_id`),
  KEY `idx_player_id` (`player_id`),
  KEY `idx_team_id` (`team_id`),
  KEY `idx_play_type_nbacom_id` (`play_type_nbacom_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `playbyplay_espn`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `playbyplay_espn` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) DEFAULT NULL,
  `period` int(11) DEFAULT NULL,
  `play_index` int(11) DEFAULT NULL,
  `deciseconds_left` int(11) DEFAULT NULL,
  `away_score` int(11) DEFAULT NULL,
  `home_score` int(11) DEFAULT NULL,
  `play_espn_id` int(11) DEFAULT NULL,
  `team_id` int(11) DEFAULT NULL,
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
  UNIQUE KEY `idx_game_play` (`game_id`,`play_index`),
  KEY `idx_game_id` (`game_id`),
  KEY `idx_player_id` (`player_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `game_stats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `game_stats` (
  `game_id` int(11) NOT NULL,
  `arena` varchar(100) DEFAULT NULL,
  `attendance` int(11) DEFAULT NULL,
  `duration` varchar(10) DEFAULT NULL,
  `local_game_start` int(11) DEFAULT NULL,
  `home_game_start` int(11) DEFAULT NULL,
  `away_game_start` int(11) DEFAULT NULL,
  `unknown_game_start` int(11) DEFAULT NULL,
  `official1` varchar(50) DEFAULT NULL,
  `official2` varchar(50) DEFAULT NULL,
  `official3` varchar(50) DEFAULT NULL,
  `national` varchar(50) DEFAULT NULL,
  `home_tv` varchar(50) DEFAULT NULL,
  `home_radio` varchar(50) DEFAULT NULL,
  `home_record` varchar(10) DEFAULT NULL,
  `home_record_conference` varchar(10) DEFAULT NULL,
  `home_record_division` varchar(10) DEFAULT NULL,
  `away_tv` varchar(50) DEFAULT NULL,
  `away_radio` varchar(50) DEFAULT NULL,
  `away_record` varchar(10) DEFAULT NULL,
  `away_record_conference` varchar(10) DEFAULT NULL,
  `away_record_division` varchar(10) DEFAULT NULL,
  `home_score` int(11) DEFAULT NULL,
  `away_score` int(11) DEFAULT NULL,
  `home_quarter_score` varchar(50) DEFAULT NULL,
  `away_quarter_score` varchar(50) DEFAULT NULL,
  `total_periods` int(11) DEFAULT NULL,
  `margin_low` int(11) DEFAULT NULL,
  `margin_high` int(11) DEFAULT NULL,
  `official1_id` int(11) DEFAULT NULL,
  `official2_id` int(11) DEFAULT NULL,
  `official3_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`game_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `player`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `player` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `old_id` int(11) DEFAULT NULL,
  `nbacom_player_id` varchar(20) DEFAULT NULL,
  `statsnbacom_player_id` int(11) DEFAULT NULL,
  `cbssports_player_id` int(11) DEFAULT NULL,
  `nbacom_player_tag` varchar(50) DEFAULT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `full_name_alt1` varchar(100) DEFAULT NULL,
  `full_name_alt2` varchar(100) DEFAULT NULL,
  `jersey_number` tinyint(4) DEFAULT NULL,
  `position` varchar(5) DEFAULT NULL,
  `current_team_id` int(11) DEFAULT NULL,
  `current_franchise_id` int(11) DEFAULT NULL,
  `date_found` date DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`),
  KEY `idx_nbacom_player_id` (`nbacom_player_id`),
  KEY `idx_cbssports_player_id` (`cbssports_player_id`),
  KEY `idx_nbacom_player_tag` (`nbacom_player_tag`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `player_cbssports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `player_cbssports` (
  `id` int(11) NOT NULL DEFAULT '0',
  `cbssports_player_id` int(11) DEFAULT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `date_found` date DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `player_nbacom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `player_nbacom` (
  `id` int(11) NOT NULL DEFAULT '0',
  `nbacom_player_id` varchar(20) DEFAULT NULL,
  `player_tag` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `date_found` date DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `player_cbssports_by_game`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `player_cbssports_by_game` (
  `id` int(11) NOT NULL DEFAULT '0',
  `game_id` int(11) DEFAULT NULL,
  `cbssports_player_id` int(11) DEFAULT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `cbs_team_code` varchar(5) DEFAULT NULL,
  `jersey_number` int(11) DEFAULT NULL,
  `position` varchar(5) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  KEY `idx_cbssports_player_id` (`cbssports_player_id`),
  KEY `idx_game_id` (`game_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `player_nbacom_by_game`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `player_nbacom_by_game` (
  `id` int(11) NOT NULL DEFAULT '0',
  `game_id` int(11) DEFAULT NULL,
  `nbacom_player_id` varchar(20) DEFAULT NULL,
  `player_id` int(11) DEFAULT NULL,
  `player_tag` varchar(50) DEFAULT NULL,
  `team_id` int(11) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `jersey_number` tinyint(4) DEFAULT NULL,
  `team` varchar(20) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  UNIQUE KEY `idx_game_nbacom_player` (`game_id`,`nbacom_player_id`),
  KEY `idx_nbacom_player_id` (`nbacom_player_id`),
  KEY `idx_game_id` (`game_id`),
  KEY `idx_player_id` (`player_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `player_team_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `player_team_history` (
  `id` int(11) NOT NULL DEFAULT '0',
  `player_id` int(11) DEFAULT NULL,
  `team_id` int(11) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `player_espn`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `player_espn` (
  `id` int(11) NOT NULL DEFAULT '0',
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
  `created_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `game`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `game` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `away_team` varchar(3) DEFAULT NULL,
  `home_team` varchar(3) DEFAULT NULL,
  `away_team_id` int(11) DEFAULT NULL,
  `home_team_id` int(11) DEFAULT NULL,
  `away_team_code` varchar(3) DEFAULT NULL,
  `home_team_code` varchar(3) DEFAULT NULL,
  `date_played` date NOT NULL,
  `abbrev` varchar(20) NOT NULL,
  `espn_game_id` int(11) DEFAULT NULL,
  `cbssports_game_id` varchar(20) DEFAULT NULL,
  `nbacom_game_id` varchar(15) DEFAULT NULL,
  `statsnbacom_game_id` varchar(16) DEFAULT NULL,
  `gametime` varchar(20) DEFAULT NULL,
  `national_tv` varchar(20) DEFAULT NULL,
  `season` varchar(10) DEFAULT NULL,
  `permalink` varchar(100) DEFAULT NULL,
  `season_type` varchar(5) DEFAULT NULL,
  `should_fetch_data` tinyint(4) DEFAULT '1',
  `dim_season_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_abbrev` (`abbrev`),
  UNIQUE KEY `idx_permalink` (`permalink`),
  KEY `idx_away_team_id` (`away_team_id`),
  KEY `idx_home_team_id` (`home_team_id`),
  KEY `idx_date_played` (`date_played`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `team`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `team` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `oldid` int(11) DEFAULT NULL,
  `franchise_id` int(11) NOT NULL,
  `code` varchar(3) NOT NULL DEFAULT '',
  `name` varchar(30) NOT NULL,
  `city` varchar(30) NOT NULL,
  `nickname` varchar(30) NOT NULL,
  `alternate_nickname` varchar(30) NOT NULL,
  `nbacom_code` char(3) DEFAULT NULL,
  `cbssports_code` varchar(3) DEFAULT NULL,
  `statsnbacom_team_id` int(11) DEFAULT NULL,
  `color1` varchar(7) DEFAULT NULL,
  `color2` varchar(7) DEFAULT NULL,
  `unique_name` varchar(40) DEFAULT NULL,
  `is_active` tinyint(4) NOT NULL DEFAULT '0',
  `alternate_nickname2` varchar(30) DEFAULT NULL,
  `division` varchar(30) DEFAULT NULL,
  `conference` varchar(30) DEFAULT NULL,
  `alternate_city` varchar(30) DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `dim_season_id` int(11) DEFAULT NULL,
  `season` varchar(10) DEFAULT NULL,
  `season_type` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `play_espn`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `play_espn` (
  `id` int(11) NOT NULL,
  `re` varchar(1000) NOT NULL,
  `name` varchar(1000) NOT NULL,
  `is_shot` tinyint(4) DEFAULT '0',
  `is_freethrow` tinyint(4) DEFAULT '0',
  `is_freethrow_last` tinyint(4) DEFAULT '0',
  `is_shot_made` tinyint(4) NOT NULL DEFAULT '0',
  `priority` smallint(6) DEFAULT '15',
  `has_player` tinyint(4) DEFAULT NULL,
  `has_player2` tinyint(4) DEFAULT NULL,
  `has_player1` tinyint(4) DEFAULT NULL,
  `is_on_floor` tinyint(4) DEFAULT NULL,
  `is_rebound` tinyint(4) DEFAULT '0',
  `is_foul` tinyint(4) DEFAULT '0',
  `is_turnover` tinyint(4) DEFAULT '0',
  `is_assist` tinyint(4) DEFAULT '0',
  `points_possible` tinyint(4) DEFAULT '0',
  `points_converted` tinyint(4) DEFAULT '0',
  `is_offensive_rebound` tinyint(4) DEFAULT '0',
  `is_steal` tinyint(4) DEFAULT '0',
  `is_timeout` tinyint(4) DEFAULT '0',
  `is_team_play` tinyint(4) DEFAULT '0',
  `is_freethrow_made` tinyint(4) DEFAULT '0',
  `is_3pt` tinyint(4) DEFAULT '0',
  `is_3pt_made` tinyint(4) DEFAULT '0',
  `is_block` tinyint(4) DEFAULT '0',
  `is_technical` tinyint(4) DEFAULT '0',
  `is_violation` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `play_type_nbacom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `play_type_nbacom` (
  `id` int(11) NOT NULL,
  `re` varchar(500) DEFAULT NULL,
  `name` varchar(200) DEFAULT NULL,
  `is_rebound` tinyint(4) DEFAULT '0',
  `is_freethrow` tinyint(4) DEFAULT '0',
  `is_shot` tinyint(4) DEFAULT '0',
  `is_shot_made` tinyint(4) DEFAULT '0',
  `is_turnover` tinyint(4) DEFAULT '0',
  `is_foul` tinyint(4) DEFAULT '0',
  `is_period_startend` tinyint(4) DEFAULT '0',
  `is_team_play` tinyint(4) DEFAULT '0',
  `is_timeout` tinyint(4) DEFAULT '0',
  `is_freethrow_made` tinyint(4) DEFAULT '0',
  `priority` tinyint(4) DEFAULT '5',
  `is_3pt` tinyint(4) DEFAULT '0',
  `is_3pt_made` tinyint(4) DEFAULT '0',
  `is_freethrow_last` tinyint(4) DEFAULT '0',
  `is_block` tinyint(4) DEFAULT '0',
  `is_assist` tinyint(4) DEFAULT '0',
  `is_steal` tinyint(4) DEFAULT '0',
  `is_violation` tinyint(4) DEFAULT '0',
  `is_technical` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `shot_type_cbssports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shot_type_cbssports` (
  `id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(50) DEFAULT NULL,
  `is_freethrow` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `shot_type_nbacom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shot_type_nbacom` (
  `id` int(11) NOT NULL DEFAULT '0',
  `nbacom_id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(100) DEFAULT NULL,
  `shot_group` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`nbacom_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `version` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `updated_at` datetime DEFAULT NULL,
  `filename` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `franchise`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `franchise` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `oldid` int(11) DEFAULT NULL,
  `code` varchar(3) NOT NULL DEFAULT '',
  `original_name` varchar(30) DEFAULT NULL,
  `original_city` varchar(30) DEFAULT NULL,
  `original_nickname` varchar(30) DEFAULT NULL,
  `current_name` varchar(30) DEFAULT NULL,
  `current_city` varchar(30) DEFAULT NULL,
  `current_nickname` varchar(30) DEFAULT NULL,
  `is_active` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `dim_play_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dim_play_type` (
  `id` int(11) NOT NULL,
  `name` varchar(1000) NOT NULL,
  `is_shot` tinyint(4) DEFAULT '0',
  `is_shot_made` tinyint(4) DEFAULT NULL,
  `is_3pt` tinyint(4) DEFAULT NULL,
  `is_3pt_made` tinyint(4) DEFAULT NULL,
  `is_freethrow` tinyint(4) DEFAULT '0',
  `is_freethrow_made` tinyint(4) DEFAULT NULL,
  `is_freethrow_last` tinyint(4) DEFAULT '0',
  `is_rebound` tinyint(4) DEFAULT '0',
  `is_offensive_rebound` tinyint(4) DEFAULT NULL,
  `is_defensive_rebound` tinyint(4) DEFAULT NULL,
  `is_foul` tinyint(4) DEFAULT '0',
  `is_turnover` tinyint(4) DEFAULT '0',
  `is_assist` tinyint(4) DEFAULT '0',
  `is_steal` tinyint(4) DEFAULT '0',
  `is_block` tinyint(4) DEFAULT '0',
  `is_technical` tinyint(4) DEFAULT '0',
  `is_violation` tinyint(4) DEFAULT '0',
  `is_timeout` tinyint(4) DEFAULT NULL,
  `is_on_floor` tinyint(4) DEFAULT NULL,
  `is_team_play` tinyint(4) DEFAULT NULL,
  `points_possible` tinyint(4) DEFAULT NULL,
  `points_converted` tinyint(4) DEFAULT NULL,
  `has_player` tinyint(4) DEFAULT NULL,
  `has_player1` tinyint(4) DEFAULT NULL,
  `has_player2` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `player_nbacom_unknown_by_game`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `player_nbacom_unknown_by_game` (
  `id` int(11) NOT NULL DEFAULT '0',
  `game_id` int(11) DEFAULT NULL,
  `nbacom_player_id` varchar(20) DEFAULT NULL,
  `player_id` int(11) DEFAULT NULL,
  `player_tag` varchar(50) DEFAULT NULL,
  `team_id` int(11) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `jersey_number` tinyint(4) DEFAULT NULL,
  `team` varchar(20) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  UNIQUE KEY `idx_game_nbacom_player` (`game_id`,`nbacom_player_id`),
  KEY `idx_nbacom_player_id` (`nbacom_player_id`),
  KEY `idx_game_id` (`game_id`),
  KEY `idx_player_id` (`player_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `shotchart_statsnbacom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shotchart_statsnbacom` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) DEFAULT NULL,
  `game_event_id` int(11) DEFAULT NULL,
  `team_id` int(11) DEFAULT NULL,
  `player_id` int(11) DEFAULT NULL,
  `period` int(11) DEFAULT NULL,
  `deciseconds_left` int(11) DEFAULT NULL,
  `x` int(11) DEFAULT NULL,
  `y` int(11) DEFAULT NULL,
  `shot_distance` int(11) DEFAULT NULL,
  `shot_attempted_flag` tinyint(4) DEFAULT NULL,
  `shot_made_flag` tinyint(4) DEFAULT NULL,
  `event_type` varchar(128) DEFAULT NULL,
  `shot_type` varchar(128) DEFAULT NULL,
  `action_type` varchar(128) DEFAULT NULL,
  `player_name` varchar(128) DEFAULT NULL,
  `statsnbacom_team_id` int(11) DEFAULT NULL,
  `statsnbacom_team_name` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `playbyplay_statsnbacom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `playbyplay_statsnbacom` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) DEFAULT NULL,
  `game_event_id` int(11) DEFAULT NULL,
  `period` int(11) DEFAULT NULL,
  `deciseconds_left` int(11) DEFAULT NULL,
  `team_id` int(11) DEFAULT NULL,
  `away_score` int(11) DEFAULT NULL,
  `home_score` int(11) DEFAULT NULL,
  `player_id` int(11) DEFAULT NULL,
  `player1_id` int(11) DEFAULT NULL,
  `player2_id` int(11) DEFAULT NULL,
  `play_type_statsnbacom_id` int(11) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `homedescription` varchar(255) DEFAULT NULL,
  `neutraldescription` varchar(255) DEFAULT NULL,
  `visitordescription` varchar(255) DEFAULT NULL,
  `eventmsgactiontype` varchar(255) DEFAULT NULL,
  `eventmsgtype` int(11) DEFAULT NULL,
  `wctimestring` varchar(64) DEFAULT NULL,
  `pctimestring` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_game_event` (`game_id`,`game_event_id`),
  KEY `idx_player_id` (`player_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `play_type_statsnbacom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `play_type_statsnbacom` (
  `id` int(11) NOT NULL,
  `re` varchar(256) DEFAULT NULL,
  `name` varchar(256) DEFAULT NULL,
  `priority` int(11) DEFAULT NULL,
  `is_shot` tinyint(4) DEFAULT '0',
  `is_shot_made` tinyint(4) DEFAULT '0',
  `is_freethrow` tinyint(4) DEFAULT '0',
  `is_freethrow_made` tinyint(4) DEFAULT '0',
  `is_freethrow_last` tinyint(4) DEFAULT '0',
  `is_rebound` tinyint(4) DEFAULT '0',
  `is_offensive_rebound` tinyint(4) DEFAULT '0',
  `is_defensive_rebound` tinyint(4) DEFAULT '0',
  `is_foul` tinyint(4) DEFAULT '0',
  `is_turnover` tinyint(4) DEFAULT '0',
  `is_assist` tinyint(4) DEFAULT '0',
  `is_steal` tinyint(4) DEFAULT '0',
  `is_block` tinyint(4) DEFAULT '0',
  `is_technical` tinyint(4) DEFAULT '0',
  `is_violation` tinyint(4) DEFAULT '0',
  `is_timeout` tinyint(4) DEFAULT '0',
  `is_on_floor` tinyint(4) DEFAULT '0',
  `is_team_play` tinyint(4) DEFAULT '0',
  `points_converted` tinyint(4) DEFAULT NULL,
  `points_possible` tinyint(4) DEFAULT NULL,
  `has_player_id` tinyint(4) DEFAULT '0',
  `has_player1_id` tinyint(4) DEFAULT '0',
  `has_player2_id` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `boxscore_statsnbacom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boxscore_statsnbacom` (
  `game_id` int(11) NOT NULL DEFAULT '0',
  `player_id` int(11) NOT NULL DEFAULT '0',
  `team_id` int(11) DEFAULT NULL,
  `deciseconds_played` int(11) DEFAULT NULL,
  `points` int(11) DEFAULT NULL,
  `rebounds` int(11) DEFAULT NULL,
  `assists` int(11) DEFAULT NULL,
  `steals` int(11) DEFAULT NULL,
  `blocks` int(11) DEFAULT NULL,
  `fouls` int(11) DEFAULT NULL,
  `turnovers` int(11) DEFAULT NULL,
  `rebounds_defensive` int(11) DEFAULT NULL,
  `rebounds_offensive` int(11) DEFAULT NULL,
  `fgm` int(11) DEFAULT NULL,
  `fga` int(11) DEFAULT NULL,
  `ftm` int(11) DEFAULT NULL,
  `fta` int(11) DEFAULT NULL,
  `threeptm` int(11) DEFAULT NULL,
  `threepta` int(11) DEFAULT NULL,
  `ft` decimal(6,3) DEFAULT NULL,
  `fg` decimal(6,3) DEFAULT NULL,
  `threeptfg` decimal(6,3) DEFAULT NULL,
  `plus_minus` int(11) DEFAULT NULL,
  `comment` varchar(100) DEFAULT NULL,
  `start_position` varchar(20) DEFAULT NULL,
  `statsnbacom_player_id` int(11) NOT NULL DEFAULT '0',
  `statsnbacom_player_name` varchar(100) DEFAULT NULL,
  `statsnbacom_game_id` int(11) DEFAULT NULL,
  `statsnbacom_team_id` int(11) DEFAULT NULL,
  `statsnbacom_team_abbreviation` varchar(50) DEFAULT NULL,
  `statsnbacom_team_city` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`game_id`,`player_id`,`statsnbacom_player_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `game_stats_statsnbacom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `game_stats_statsnbacom` (
  `game_id` int(11) NOT NULL,
  `attendance` int(11) DEFAULT NULL,
  `duration` varchar(20) DEFAULT NULL,
  `official1_id` int(11) DEFAULT NULL,
  `official2_id` int(11) DEFAULT NULL,
  `official3_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`game_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `game_stats_team_statsnbacom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `game_stats_team_statsnbacom` (
  `game_id` int(11) NOT NULL DEFAULT '0',
  `team_id` int(11) NOT NULL DEFAULT '0',
  `deciseconds_elapsed` int(11) DEFAULT NULL,
  `points` int(11) DEFAULT NULL,
  `rebounds` int(11) DEFAULT NULL,
  `assists` int(11) DEFAULT NULL,
  `steals` int(11) DEFAULT NULL,
  `blocks` int(11) DEFAULT NULL,
  `fouls` int(11) DEFAULT NULL,
  `turnovers` int(11) DEFAULT NULL,
  `rebounds_defensive` int(11) DEFAULT NULL,
  `rebounds_offensive` int(11) DEFAULT NULL,
  `fgm` int(11) DEFAULT NULL,
  `fga` int(11) DEFAULT NULL,
  `ftm` int(11) DEFAULT NULL,
  `fta` int(11) DEFAULT NULL,
  `threeptm` int(11) DEFAULT NULL,
  `threepta` int(11) DEFAULT NULL,
  `ft` decimal(6,3) DEFAULT NULL,
  `fg` decimal(6,3) DEFAULT NULL,
  `threeptfg` decimal(6,3) DEFAULT NULL,
  `plus_minus` int(11) DEFAULT NULL,
  `lead_changes` int(11) DEFAULT NULL,
  `points_second_chance` int(11) DEFAULT NULL,
  `points_in_paint` int(11) DEFAULT NULL,
  `points_fb` int(11) DEFAULT NULL,
  `times_tied` int(11) DEFAULT NULL,
  `largest_lead` int(11) DEFAULT NULL,
  `pts_qtr1` int(11) DEFAULT NULL,
  `pts_qtr2` int(11) DEFAULT NULL,
  `pts_qtr3` int(11) DEFAULT NULL,
  `pts_qtr4` int(11) DEFAULT NULL,
  `pts_ot1` int(11) DEFAULT NULL,
  `pts_ot2` int(11) DEFAULT NULL,
  `pts_ot3` int(11) DEFAULT NULL,
  `pts_ot4` int(11) DEFAULT NULL,
  `pts_ot5` int(11) DEFAULT NULL,
  `pts_ot6` int(11) DEFAULT NULL,
  `pts_ot7` int(11) DEFAULT NULL,
  `pts_ot8` int(11) DEFAULT NULL,
  `pts_ot9` int(11) DEFAULT NULL,
  `pts_ot10` int(11) DEFAULT NULL,
  `team_wins_losses` varchar(20) DEFAULT NULL,
  `game_sequence` int(11) DEFAULT NULL,
  `statsnbacom_game_id` int(11) DEFAULT NULL,
  `statsnbacom_team_id` int(11) DEFAULT NULL,
  `statsnbacom_team_abbreviation` varchar(50) DEFAULT NULL,
  `statsnbacom_team_city` varchar(50) DEFAULT NULL,
  `statsnbacom_team_name` varchar(50) DEFAULT NULL,
  `statsnbacom_season_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`game_id`,`team_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `player_statsnbacom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `player_statsnbacom` (
  `statsnbacom_player_id` int(11) NOT NULL DEFAULT '0',
  `game_id` int(11) NOT NULL DEFAULT '0',
  `statsnbacom_team_id` int(11) DEFAULT NULL,
  `statsnbacom_player_name` varchar(100) DEFAULT NULL,
  `player_id` int(11) DEFAULT NULL,
  `team_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`statsnbacom_player_id`,`game_id`)
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

