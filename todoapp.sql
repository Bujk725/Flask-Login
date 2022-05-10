-- phpMyAdmin SQL Dump
-- version 4.9.7
-- https://www.phpmyadmin.net/
--
-- Anamakine: 127.0.0.1:3306
-- Üretim Zamanı: 10 May 2022, 20:51:09
-- Sunucu sürümü: 5.7.36
-- PHP Sürümü: 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Veritabanı: `todoapp`
--

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `todo`
--

DROP TABLE IF EXISTS `todo`;
CREATE TABLE IF NOT EXISTS `todo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `todo_head_id` int(11) NOT NULL,
  `content` text COLLATE utf8_turkish_ci NOT NULL,
  `complete` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

--
-- Tablo döküm verisi `todo`
--

INSERT INTO `todo` (`id`, `todo_head_id`, `content`, `complete`) VALUES
(1, 1, 'Flask Öğrenilecek', 1),
(2, 1, 'Django Öğrenilecek', 0),
(3, 1, 'Flask Web Site Örneği', 1),
(4, 2, 'Jquery', 0),
(5, 2, 'Dom', 0);

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `todo_head`
--

DROP TABLE IF EXISTS `todo_head`;
CREATE TABLE IF NOT EXISTS `todo_head` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` text COLLATE utf8_turkish_ci NOT NULL,
  `created_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `category` text COLLATE utf8_turkish_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

--
-- Tablo döküm verisi `todo_head`
--

INSERT INTO `todo_head` (`id`, `title`, `created_date`, `category`) VALUES
(1, 'Python', '2022-05-09 12:54:28', 'İş'),
(2, 'Javascript', '2022-05-09 12:54:28', 'Hobi');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` text COLLATE utf8_turkish_ci NOT NULL,
  `name` text COLLATE utf8_turkish_ci NOT NULL,
  `lastname` text COLLATE utf8_turkish_ci NOT NULL,
  `password` text COLLATE utf8_turkish_ci NOT NULL,
  `email` text COLLATE utf8_turkish_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

--
-- Tablo döküm verisi `users`
--

INSERT INTO `users` (`id`, `username`, `name`, `lastname`, `password`, `email`) VALUES
(1, 'bujk725', 'burak', 'özlece', '123', 'burak@gmail.com'),
(2, 'yusuff', 'yusuf', 'altuntaş', '1234', 'yusuf@gmail.com');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `users_todo_head`
--

DROP TABLE IF EXISTS `users_todo_head`;
CREATE TABLE IF NOT EXISTS `users_todo_head` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userID` int(11) NOT NULL,
  `todo_head_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

--
-- Tablo döküm verisi `users_todo_head`
--

INSERT INTO `users_todo_head` (`id`, `userID`, `todo_head_id`) VALUES
(1, 1, 1),
(2, 2, 1),
(3, 2, 2);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
