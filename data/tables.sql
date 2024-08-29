-- MySQL dump 10.13  Distrib 8.0.39, for Linux (x86_64)
--
-- Host: localhost    Database: vt_scan
-- ------------------------------------------------------
-- Server version	8.0.39-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `main_urls`
--

DROP TABLE IF EXISTS `main_urls`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_urls` (
  `id` int NOT NULL AUTO_INCREMENT,
  `url_hash` char(64) NOT NULL,
  `url` varchar(2047) NOT NULL,
  `last_scanned` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `url_hash` (`url_hash`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ms_urls`
--

DROP TABLE IF EXISTS `ms_urls`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ms_urls` (
  `main_url_id` int NOT NULL,
  `scanned_url_id` int NOT NULL,
  PRIMARY KEY (`main_url_id`,`scanned_url_id`),
  KEY `ms_urls_ibfk_2` (`scanned_url_id`),
  CONSTRAINT `ms_urls_ibfk_1` FOREIGN KEY (`main_url_id`) REFERENCES `main_urls` (`id`) ON DELETE CASCADE,
  CONSTRAINT `ms_urls_ibfk_2` FOREIGN KEY (`scanned_url_id`) REFERENCES `scanned_urls` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `report_results`
--

DROP TABLE IF EXISTS `report_results`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `report_results` (
  `scanned_url_id` int NOT NULL,
  `engine_name` varchar(255) DEFAULT NULL,
  `method` varchar(50) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `result` varchar(50) DEFAULT NULL,
  UNIQUE KEY `scanned_url_id` (`scanned_url_id`,`engine_name`),
  CONSTRAINT `report_results_ibfk_1` FOREIGN KEY (`scanned_url_id`) REFERENCES `scanned_urls` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `scanned_urls`
--

DROP TABLE IF EXISTS `scanned_urls`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `scanned_urls` (
  `id` int NOT NULL AUTO_INCREMENT,
  `url_hash` char(64) NOT NULL,
  `url` varchar(2047) DEFAULT NULL,
  `malicious` int DEFAULT '0',
  `suspicious` int DEFAULT '0',
  `undetected` int DEFAULT '0',
  `harmless` int DEFAULT '0',
  `timeout` int DEFAULT '0',
  `last_scanned` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `url_hash` (`url_hash`)
) ENGINE=InnoDB AUTO_INCREMENT=160 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-08-28 16:41:20
