-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 18, 2026 at 08:41 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ideahub_pos`
--

-- --------------------------------------------------------

--
-- Table structure for table `boardroom_bookings`
--

CREATE TABLE `boardroom_bookings` (
  `id` int(11) NOT NULL,
  `customer_name` varchar(100) NOT NULL,
  `date` date NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `number_of_people` int(11) NOT NULL,
  `purpose` varchar(255) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `session_id` int(11) DEFAULT NULL,
  `started_at` datetime DEFAULT NULL,
  `expected_end_at` datetime DEFAULT NULL,
  `ended_at` datetime DEFAULT NULL,
  `extended_minutes` int(11) NOT NULL DEFAULT 0,
  `course` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `boardroom_bookings`
--

INSERT INTO `boardroom_bookings` (`id`, `customer_name`, `date`, `start_time`, `end_time`, `number_of_people`, `purpose`, `status`, `created_at`, `session_id`, `started_at`, `expected_end_at`, `ended_at`, `extended_minutes`, `course`) VALUES
(1, 'CarltestBook', '2026-04-28', '20:00:00', '20:15:00', 5, 'Sutdy', 'completed', '2026-04-28 12:00:01', 1, '2026-04-28 12:00:44', '2026-04-28 20:15:00', '2026-04-28 12:06:59', 10, NULL),
(2, 'cac', '2026-04-28', '07:00:00', '08:00:00', 12, '', 'cancelled', '2026-04-28 12:08:44', NULL, NULL, '2026-04-28 08:00:00', NULL, 0, NULL),
(3, 'carl22', '2026-04-28', '07:00:00', '10:00:00', 10, 'study', 'completed', '2026-04-28 12:13:20', 2, '2026-04-28 12:14:14', '2026-04-28 10:00:00', '2026-04-28 12:17:41', 60, 'it'),
(4, 'carlss', '2026-04-28', '09:00:00', '14:00:00', 20, 'sleep', 'cancelled', '2026-04-28 12:14:09', NULL, NULL, '2026-04-28 14:00:00', NULL, 0, 'it'),
(5, 'gg', '2026-05-08', '20:02:00', '20:30:00', 4, 'STUDY', 'completed', '2026-05-08 12:02:23', 9, '2026-05-08 12:02:27', '2026-05-08 20:30:00', '2026-05-08 12:13:11', 0, 'IT'),
(6, 'asdasf', '2026-05-09', '07:00:00', '08:00:00', 2, '', 'cancelled', '2026-05-08 14:56:56', NULL, NULL, '2026-05-09 08:00:00', NULL, 0, 'asf'),
(7, 'sir', '2026-05-18', '07:00:00', '21:00:00', 4, 'study', 'completed', '2026-05-18 04:41:47', 17, '2026-05-18 04:43:40', '2026-05-18 21:00:00', '2026-05-18 05:30:28', 60, 'it');

-- --------------------------------------------------------

--
-- Table structure for table `customer_sessions`
--

CREATE TABLE `customer_sessions` (
  `id` int(11) NOT NULL,
  `customer_name` varchar(100) NOT NULL,
  `school` varchar(100) DEFAULT NULL,
  `course` varchar(100) DEFAULT NULL,
  `space_type_id` int(11) NOT NULL,
  `time_in` datetime NOT NULL,
  `time_out` datetime DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `number_of_people` int(11) NOT NULL DEFAULT 1,
  `payment_method` varchar(50) DEFAULT 'cash',
  `amount_tendered` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customer_sessions`
--

INSERT INTO `customer_sessions` (`id`, `customer_name`, `school`, `course`, `space_type_id`, `time_in`, `time_out`, `status`, `number_of_people`, `payment_method`, `amount_tendered`) VALUES
(1, 'CarltestBook', 'Boardroom Booking', 'Sutdy', 3, '2026-04-28 12:00:44', '2026-04-28 12:06:59', 'completed', 1, 'cash', NULL),
(2, 'carl22', 'Boardroom Booking', 'it', 3, '2026-04-28 12:14:14', '2026-04-28 12:17:41', 'completed', 1, 'cash', NULL),
(3, 'carfl', 'ui', 'it', 2, '2026-04-28 13:33:58', '2026-04-28 13:34:09', 'completed', 1, 'cash', NULL),
(4, 'regular1', 'ui', 'it', 1, '2026-04-28 14:00:57', '2026-04-28 14:02:48', 'completed', 2, 'cash', NULL),
(5, 'carls', 'ui', 'it', 2, '2026-04-28 14:03:41', '2026-04-28 14:04:46', 'completed', 1, 'cash', NULL),
(6, 'carl', 'ui', 'it', 2, '2026-04-29 14:31:11', '2026-04-29 14:49:19', 'completed', 1, 'cash', NULL),
(7, 'carlgwapo', 'ui', 'it', 2, '2026-05-06 13:49:05', '2026-05-06 14:16:49', 'completed', 1, 'cash', NULL),
(8, 'carlsssadas', 'Ui', 'IT', 2, '2026-05-07 12:54:44', '2026-05-07 13:10:26', 'completed', 1, 'cash', NULL),
(9, 'gg', 'Boardroom Booking', 'IT', 3, '2026-05-08 12:02:27', '2026-05-08 12:13:11', 'completed', 4, 'cash', NULL),
(10, 'gsss', 'ui', 'it', 3, '2026-05-08 12:02:47', '2026-05-08 12:13:08', 'completed', 1, 'cash', NULL),
(11, 'car', 'ui', 'it', 2, '2026-05-08 14:45:55', '2026-05-08 14:57:23', 'completed', 1, 'cash', NULL),
(12, 'carl', 'ui', 'iy', 2, '2026-05-10 08:26:19', '2026-05-10 09:51:31', 'completed', 1, 'cash', NULL),
(13, 'asdasdas', 'asd', 'ui', 2, '2026-05-10 10:06:04', '2026-05-12 07:10:12', 'completed', 1, 'cash', NULL),
(14, 'sss', 'ss', 's', 1, '2026-05-12 07:29:52', '2026-05-12 08:39:30', 'completed', 1, 'cash', NULL),
(15, 'kurt', 'ui', 'it', 1, '2026-05-12 12:54:28', NULL, 'active', 1, 'cash', NULL),
(16, 'puala', 'ui', 'it', 2, '2026-05-18 04:34:28', NULL, 'active', 1, 'cash', NULL),
(17, 'sir', 'Boardroom Booking', 'it', 3, '2026-05-18 04:43:40', '2026-05-18 05:30:28', 'completed', 4, 'cash', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `daily_sales_reports`
--

CREATE TABLE `daily_sales_reports` (
  `id` int(11) NOT NULL,
  `report_date` date NOT NULL,
  `total_revenue` decimal(12,2) NOT NULL,
  `total_expenses` decimal(12,2) NOT NULL,
  `net_balance` decimal(12,2) NOT NULL,
  `total_orders` int(11) NOT NULL,
  `total_sessions` int(11) NOT NULL,
  `generated_by` int(11) NOT NULL,
  `generated_at` datetime DEFAULT NULL,
  `notes` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `daily_sales_reports`
--

INSERT INTO `daily_sales_reports` (`id`, `report_date`, `total_revenue`, `total_expenses`, `net_balance`, `total_orders`, `total_sessions`, `generated_by`, `generated_at`, `notes`) VALUES
(1, '2026-05-08', 1706.76, 240.00, 1466.76, 3, 3, 2, '2026-05-08 12:12:24', 'NA'),
(8, '2026-05-07', 330.24, 0.00, 330.24, 2, 1, 2, '2026-05-08 12:13:49', 'TRY'),
(9, '2026-05-12', 3397.90, 1030.00, 2367.90, 1, 1, 2, '2026-05-12 07:52:27', 'soft balancing for todayts 5/12/26 AM'),
(10, '2026-05-18', 0.00, 0.00, 0.00, 2, 2, 2, '2026-05-18 04:55:59', 'trying\n');

-- --------------------------------------------------------

--
-- Table structure for table `departments`
--

CREATE TABLE `departments` (
  `name` varchar(120) NOT NULL,
  `id` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `departments`
--

INSERT INTO `departments` (`name`, `id`, `created_at`, `updated_at`) VALUES
('Operations', 1, '2026-05-08 14:29:08', '2026-05-08 14:29:08'),
('Finance', 2, '2026-05-08 14:29:08', '2026-05-08 14:29:08'),
('Technology', 3, '2026-05-08 14:29:08', '2026-05-08 14:29:08');

-- --------------------------------------------------------

--
-- Table structure for table `expenses`
--

CREATE TABLE `expenses` (
  `id` int(11) NOT NULL,
  `category` varchar(50) NOT NULL,
  `description` text NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `expense_date` date NOT NULL,
  `logged_by` int(11) NOT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `expenses`
--

INSERT INTO `expenses` (`id`, `category`, `description`, `amount`, `expense_date`, `logged_by`, `created_at`) VALUES
(4, 'food', 'CHICKEN', 240.00, '2026-05-08', 2, '2026-05-08 15:09:24'),
(5, 'supplies', 'water delivery', 540.00, '2026-05-12', 2, '2026-05-12 08:34:21'),
(6, 'supplies', 'chicken breast', 490.00, '2026-05-12', 2, '2026-05-12 12:23:25'),
(7, 'transport', 'pleti', 50.00, '2026-05-18', 2, '2026-05-18 05:29:13');

-- --------------------------------------------------------

--
-- Table structure for table `finance_budgets`
--

CREATE TABLE `finance_budgets` (
  `name` varchar(120) NOT NULL,
  `total_budget` decimal(12,2) NOT NULL,
  `allocated` decimal(12,2) NOT NULL,
  `id` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `finance_budgets`
--

INSERT INTO `finance_budgets` (`name`, `total_budget`, `allocated`, `id`, `created_at`, `updated_at`) VALUES
('Main Budget', 0.00, 0.00, 1, '2026-05-08 14:29:08', '2026-05-08 14:29:08');

-- --------------------------------------------------------

--
-- Table structure for table `finance_transactions`
--

CREATE TABLE `finance_transactions` (
  `budget_id` int(11) NOT NULL,
  `type` varchar(30) NOT NULL,
  `amount` decimal(12,2) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `id` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `finance_transactions`
--

INSERT INTO `finance_transactions` (`budget_id`, `type`, `amount`, `description`, `id`, `created_at`, `updated_at`) VALUES
(1, 'expense', 10.00, 'smoke-test', 1, '2026-05-08 14:29:09', '2026-05-08 14:29:09'),
(1, 'expense', 10.00, 'smoke-test', 2, '2026-05-08 14:29:37', '2026-05-08 14:29:37'),
(1, 'expense', 10.00, 'smoke-test', 3, '2026-05-08 14:30:56', '2026-05-08 14:30:56'),
(1, 'expense', 10.00, 'smoke-test', 4, '2026-05-08 14:42:25', '2026-05-08 14:42:25'),
(1, 'expense', 10.00, 'smoke-test', 5, '2026-05-08 15:02:49', '2026-05-08 15:02:49'),
(1, 'expense', 10.00, 'smoke-test', 6, '2026-05-08 15:06:18', '2026-05-08 15:06:18');

-- --------------------------------------------------------

--
-- Table structure for table `ideas`
--

CREATE TABLE `ideas` (
  `title` varchar(200) NOT NULL,
  `description` text DEFAULT NULL,
  `status` varchar(30) NOT NULL,
  `department_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `id` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ideas`
--

INSERT INTO `ideas` (`title`, `description`, `status`, `department_id`, `user_id`, `id`, `created_at`, `updated_at`) VALUES
('Queue Improvement', 'Improve checkout queue handoff.', 'pending', 1, 2, 1, '2026-05-08 14:29:09', '2026-05-08 14:29:09'),
('Self-order Kiosk', 'Add guided ordering tablets.', 'approved', 2, 2, 2, '2026-05-08 14:29:09', '2026-05-08 14:29:09'),
('Supplier Alerts', 'Email alert for low stock.', 'pending', 3, 2, 3, '2026-05-08 14:29:09', '2026-05-08 14:29:09'),
('Expense Auto-tagging', 'Auto-categorize finance entries.', 'rejected', 1, 2, 4, '2026-05-08 14:29:09', '2026-05-08 14:29:09'),
('Loyalty Program', 'Points for returning lounge users.', 'approved', 2, 2, 5, '2026-05-08 14:29:09', '2026-05-08 14:29:09');

-- --------------------------------------------------------

--
-- Table structure for table `idea_votes`
--

CREATE TABLE `idea_votes` (
  `idea_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `is_upvote` tinyint(1) NOT NULL,
  `id` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `inventory_items`
--

CREATE TABLE `inventory_items` (
  `id` int(11) NOT NULL,
  `menu_item_id` int(11) NOT NULL,
  `stock_qty` int(11) NOT NULL,
  `low_stock_threshold` int(11) NOT NULL,
  `unit` varchar(50) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inventory_items`
--

INSERT INTO `inventory_items` (`id`, `menu_item_id`, `stock_qty`, `low_stock_threshold`, `unit`, `created_at`, `updated_at`) VALUES
(1, 70, 10, 2, 'kg', '2026-05-08 14:42:25', '2026-05-08 14:42:25'),
(2, 70, 2, 2, 'kg', '2026-05-08 15:02:47', '2026-05-10 09:10:04'),
(3, 70, 10, 2, 'kg', '2026-05-08 15:06:17', '2026-05-08 15:06:17'),
(4, 52, 1, 5, 'pieces', '2026-05-08 15:11:44', '2026-05-13 13:39:15'),
(6, 77, 50, 10, 'pieces', '2026-05-18 04:45:31', '2026-05-18 04:45:31');

-- --------------------------------------------------------

--
-- Table structure for table `inventory_logs`
--

CREATE TABLE `inventory_logs` (
  `id` int(11) NOT NULL,
  `inventory_item_id` int(11) NOT NULL,
  `change_qty` int(11) NOT NULL,
  `reason` varchar(100) NOT NULL,
  `changed_by` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inventory_logs`
--

INSERT INTO `inventory_logs` (`id`, `inventory_item_id`, `change_qty`, `reason`, `changed_by`, `created_at`) VALUES
(1, 2, -8, 'Expired', 2, '2026-05-10 09:10:04'),
(5, 4, -1, 'Order deduction', NULL, '2026-05-13 13:39:15');

-- --------------------------------------------------------

--
-- Table structure for table `lounge_bookings`
--

CREATE TABLE `lounge_bookings` (
  `id` int(11) NOT NULL,
  `customer_name` varchar(100) NOT NULL,
  `date` date NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `number_of_people` int(11) NOT NULL,
  `purpose` varchar(255) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `menu_items`
--

CREATE TABLE `menu_items` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `is_available` tinyint(1) DEFAULT 1,
  `description` text DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `menu_items`
--

INSERT INTO `menu_items` (`id`, `name`, `price`, `category`, `status`, `image_url`, `is_available`, `description`, `created_at`, `updated_at`) VALUES
(1, 'Tapsilog', 95.00, 'MainDish - Silog', 'active', NULL, 0, NULL, '2026-05-10 18:13:44', '2026-05-14 08:29:30'),
(2, 'Longsilog', 95.00, 'MainDish - Silog', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(3, 'Hotsilog', 90.00, 'MainDish - Silog', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(4, 'Tocilog', 90.00, 'MainDish - Silog', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(5, 'Chicksilog', 105.00, 'MainDish - Silog', 'active', NULL, 0, NULL, '2026-05-10 18:13:44', '2026-05-14 08:22:30'),
(6, 'Spamsilog', 95.00, 'MainDish - Silog', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(7, 'Cornsilog', 85.00, 'MainDish - Silog', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(8, 'Bangsilog', 120.00, 'MainDish - Silog', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(9, 'Sisig Silog', 115.00, 'MainDish - Silog', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(10, 'Adobo', 65.00, NULL, 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-14 08:40:37'),
(11, 'Fried Chicken', 110.00, 'Main Dish', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(12, 'Grilled Liempo', 130.00, 'MainDish - Main Meals', 'active', NULL, 0, NULL, '2026-05-10 18:13:44', '2026-05-14 08:21:01'),
(13, 'Kare-Kare', 120.00, 'MainDish - Main Meals', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(14, 'Bulalo', 140.00, 'MainDish - Main Meals', 'active', NULL, 0, NULL, '2026-05-10 18:13:44', '2026-05-14 08:45:36'),
(15, 'Beef Caldereta', 125.00, 'MainDish - Main Meals', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(16, 'Burger', 50.00, 'MainDish - Modern Meals', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(17, 'Chicken Sandwich', 85.00, 'Side Dish', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(18, 'Sisig Bowl', 140.00, 'Main Dish', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(19, 'Chicken Alfredo Bowl', 130.00, 'Main Dish', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(20, 'Pesto Chicken Bowl', 120.00, 'Main Dish', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(21, 'Pancit Canton', 75.00, 'Snacks - Pancit', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(22, 'Pancit Bihon', 75.00, 'Snacks - Pancit', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(23, 'Pancit Malabon', 95.00, 'Snacks - Pancit', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(26, 'Onion Rings', 60.00, 'Snacks - Fries & Sides', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(27, 'Chicken Nuggets', 80.00, 'Snacks - Fries & Sides', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(28, 'Siomai', 70.00, 'Snacks - Fries & Sides', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(29, 'Kikiam', 65.00, 'Snacks - Fries & Sides', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(30, 'Lumpia Shanghai', 80.00, 'Snacks - Appetizers', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(31, 'Chicharon Bulaklak', 85.00, 'Snacks - Appetizers', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(32, 'Isaw', 90.00, 'Snacks - Appetizers', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(33, 'Takoyaki', 95.00, 'Snacks - Appetizers', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(34, 'Halo-Halo', 90.00, 'Snacks - Desserts', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(35, 'Leche Flan', 80.00, 'Snacks - Desserts', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(37, 'Hot Americano', 60.00, 'Drinks - Coffee (Hot)', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(38, 'Hot Latte', 80.00, 'Drinks - Coffee (Hot)', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(39, 'Hot Mocha', 95.00, 'Drinks - Coffee (Hot)', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(40, 'Hot Chocolate', 100.00, 'Drinks - Coffee (Hot)', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(41, 'Iced Americano', 65.00, 'Drinks - Coffee (Cold)', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(42, 'Iced Latte', 95.00, 'Drinks - Coffee (Cold)', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(43, 'Iced Mocha', 110.00, 'Drinks - Coffee (Cold)', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(44, 'Iced Chocolate', 110.00, 'Drinks - Coffee (Cold)', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(45, 'Pineapple Juice', 60.00, 'Drinks - Juices', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(46, 'Calamansi Juice', 60.00, 'Drinks - Juices', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(47, 'Orange Juice', 65.00, 'Drinks - Juices', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(48, 'Mango Shake', 90.00, 'Drinks - Juices', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(49, 'Banana Milk', 75.00, 'Drinks - Juices', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(50, 'Coke', 35.00, 'Drinks - Soft Drinks', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(51, 'Royal', 35.00, 'Drinks - Soft Drinks', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(52, 'Sprite', 35.00, 'Drinks - Soft Drinks', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(53, 'Juice', 30.00, 'Drinks - Juices', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(54, 'Coffee', 40.00, 'Drinks - Coffee (Cold)', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(55, 'Fries', 40.00, 'Snack', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-14 08:25:43'),
(56, 'Hot Cappuccino', 85.00, 'Coffee - Hot', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(57, 'Iced Cappuccino', 100.00, 'Coffee - Cold', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(58, 'Strawberry Juice', 70.00, 'Juices', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(59, 'Watermelon Juice', 65.00, 'Juices', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(60, 'Mineral Water (500ml)', 20.00, 'Bottled Water', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(61, 'Mineral Water (1L)', 35.00, 'Bottled Water', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(62, 'Spring Water (500ml)', 18.00, 'Bottled Water', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(63, 'Hot Cappuccino', 85.00, 'Coffee - Hot', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(64, 'Iced Cappuccino', 100.00, 'Coffee - Cold', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(65, 'Strawberry Juice', 70.00, 'Juices', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(66, 'Watermelon Juice', 65.00, 'Juices', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(67, 'Mineral Water (500ml)', 20.00, 'Bottled Water', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(68, 'Mineral Water (1L)', 35.00, 'Bottled Water', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(69, 'Spring Water (500ml)', 18.00, 'Bottled Water', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(70, 'chicken test', 0.00, 'ingredient', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(71, 'Smoke Menu', 1.00, 'Test', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(72, 'Smoke Menu', 1.00, 'Test', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(73, 'Smoke Menu', 1.00, 'Test', 'active', NULL, 1, NULL, '2026-05-10 18:13:44', '2026-05-10 18:13:44'),
(74, 'Siomai Rice', 60.00, 'Snack', 'active', '/static/uploads/menu/menu_f375ba6ff8224525a85b3ffd4d17fced.jpg', 1, NULL, '2026-05-12 08:02:55', '2026-05-14 08:22:39'),
(75, 'Garlic Fries', 55.00, 'Snacks - Fries & Sides', 'active', NULL, 1, NULL, '2026-05-12 08:10:33', '2026-05-12 08:10:33'),
(77, 'Banana Cue', 50.00, 'Snacks - Desserts', 'active', NULL, 1, NULL, '2026-05-15 07:58:51', '2026-05-15 07:58:51');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `customer_session_id` int(11) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `handled_by` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `customer_session_id`, `created_at`, `status`, `handled_by`) VALUES
(1, 1, '2026-04-28 12:01:13', 'done', 2),
(2, 1, '2026-04-28 12:02:07', 'done', 2),
(3, 5, '2026-04-28 14:04:07', 'done', NULL),
(4, 6, '2026-04-29 14:48:38', 'done', NULL),
(5, 7, '2026-05-06 13:49:16', 'done', 2),
(6, 7, '2026-05-06 14:16:43', 'preparing', 2),
(7, 8, '2026-05-07 12:55:15', 'done', 2),
(8, 8, '2026-05-07 12:55:38', 'done', 2),
(9, 9, '2026-05-08 12:12:43', 'done', 2),
(10, 10, '2026-05-08 12:12:51', 'done', 2),
(11, 11, '2026-05-08 14:47:39', 'done', 2),
(12, 13, '2026-05-12 07:09:48', 'done', 2),
(13, 14, '2026-05-12 08:36:12', 'done', 2),
(14, 15, '2026-05-13 13:39:15', 'done', 10),
(15, 15, '2026-05-13 14:23:25', 'done', 2),
(16, 16, '2026-05-18 04:37:37', 'done', 2),
(17, 17, '2026-05-18 04:44:02', 'done', 2);

-- --------------------------------------------------------

--
-- Table structure for table `order_items`
--

CREATE TABLE `order_items` (
  `id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `menu_item_id` int(11) NOT NULL,
  `quantity` int(11) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `status` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `order_items`
--

INSERT INTO `order_items` (`id`, `order_id`, `menu_item_id`, `quantity`, `price`, `status`) VALUES
(1, 1, 1, 3, 95.00, 'done'),
(2, 1, 2, 2, 95.00, 'done'),
(3, 1, 16, 1, 50.00, 'done'),
(4, 1, 37, 2, 60.00, 'done'),
(5, 2, 28, 3, 70.00, 'done'),
(6, 3, 5, 1, 105.00, 'done'),
(7, 3, 11, 1, 110.00, 'done'),
(8, 3, 45, 1, 60.00, 'done'),
(9, 4, 60, 1, 20.00, 'done'),
(10, 4, 41, 1, 65.00, 'done'),
(11, 4, 10, 1, 60.00, 'done'),
(12, 4, 11, 1, 110.00, 'done'),
(13, 4, 28, 1, 70.00, 'done'),
(14, 4, 55, 1, 35.00, 'done'),
(15, 4, 22, 1, 75.00, 'done'),
(16, 5, 2, 1, 95.00, 'done'),
(17, 6, 3, 1, 90.00, 'preparing'),
(18, 7, 10, 1, 60.00, 'done'),
(19, 7, 15, 1, 125.00, 'done'),
(20, 8, 14, 1, 140.00, 'done'),
(21, 9, 15, 1, 125.00, 'done'),
(22, 9, 14, 2, 140.00, 'done'),
(23, 9, 12, 2, 130.00, 'done'),
(24, 10, 14, 3, 140.00, 'done'),
(25, 11, 15, 2, 125.00, 'done'),
(26, 11, 14, 2, 140.00, 'done'),
(27, 12, 15, 1, 125.00, 'done'),
(28, 12, 14, 2, 140.00, 'done'),
(29, 12, 48, 6, 90.00, 'done'),
(30, 13, 32, 5, 90.00, 'done'),
(31, 13, 33, 3, 95.00, 'done'),
(32, 13, 30, 3, 80.00, 'done'),
(33, 13, 31, 5, 85.00, 'done'),
(34, 13, 50, 4, 35.00, 'done'),
(35, 14, 74, 1, 60.00, 'done'),
(36, 14, 44, 1, 110.00, 'done'),
(37, 14, 52, 1, 35.00, 'done'),
(38, 14, 12, 1, 130.00, 'done'),
(39, 15, 47, 1, 65.00, 'done'),
(40, 16, 61, 1, 35.00, 'done'),
(41, 16, 68, 1, 35.00, 'done'),
(42, 17, 41, 2, 65.00, 'done'),
(43, 17, 37, 2, 60.00, 'done');

-- --------------------------------------------------------

--
-- Table structure for table `receivables`
--

CREATE TABLE `receivables` (
  `id` int(11) NOT NULL,
  `customer_name` varchar(100) NOT NULL,
  `customer_contact` varchar(100) DEFAULT NULL,
  `items_description` text NOT NULL,
  `amount_owed` decimal(10,2) NOT NULL,
  `due_date` date NOT NULL,
  `paid` tinyint(1) NOT NULL,
  `partial_paid` decimal(10,2) NOT NULL,
  `created_by` int(11) NOT NULL,
  `session_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `receivables`
--

INSERT INTO `receivables` (`id`, `customer_name`, `customer_contact`, `items_description`, `amount_owed`, `due_date`, `paid`, `partial_paid`, `created_by`, `session_id`, `created_at`) VALUES
(1, 'george', '090-900-891243', 'TAKES TUBIG BEEF CALDERITA AND BULALO AND RICE', 650.00, '2026-05-08', 1, 0.00, 2, NULL, '2026-05-08 15:08:45'),
(2, 'mix', '097890789240', 'siomai rice', 250.00, '2026-05-12', 1, 0.00, 2, NULL, '2026-05-12 08:35:07'),
(3, 'aj', '09087860', 'red horse', 340.00, '2026-05-15', 1, 0.00, 2, NULL, '2026-05-12 12:24:10'),
(4, 'june', '099788738', 'test', 134.00, '2026-05-13', 1, 0.00, 2, NULL, '2026-05-13 13:40:02'),
(5, 'tessss', '3455', 'asdsa', 3435.00, '2026-05-13', 1, 0.00, 2, NULL, '2026-05-13 13:46:32'),
(6, 'joish', '0997478948', 'coffee ', 544.00, '2026-05-14', 1, 0.00, 2, NULL, '2026-05-13 14:17:35'),
(7, 'paula', '0980-89009', 'water', 340.00, '2026-05-15', 1, 0.00, 2, NULL, '2026-05-14 07:30:01'),
(8, 'paulo', '9090898990-89', 'food', 340.00, '2026-05-14', 1, 0.00, 2, NULL, '2026-05-14 07:40:27');

-- --------------------------------------------------------

--
-- Table structure for table `reservations`
--

CREATE TABLE `reservations` (
  `id` int(11) NOT NULL,
  `customer_name` varchar(100) NOT NULL,
  `customer_contact` varchar(100) DEFAULT NULL,
  `space_type_id` int(11) NOT NULL,
  `reserved_date` date NOT NULL,
  `reserved_time` time NOT NULL,
  `duration_minutes` int(11) NOT NULL,
  `number_of_people` int(11) NOT NULL,
  `status` varchar(20) NOT NULL,
  `notes` text DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reservations`
--

INSERT INTO `reservations` (`id`, `customer_name`, `customer_contact`, `space_type_id`, `reserved_date`, `reserved_time`, `duration_minutes`, `number_of_people`, `status`, `notes`, `created_at`) VALUES
(1, 'Smoke', '0912', 1, '2026-05-08', '10:00:00', 60, 1, 'cancelled', NULL, '2026-05-08 14:42:25'),
(2, 'Smoke', '0912', 1, '2026-05-08', '10:00:00', 60, 1, 'cancelled', NULL, '2026-05-08 15:02:48'),
(3, 'Smoke', '0912', 1, '2026-05-08', '10:00:00', 60, 1, 'cancelled', NULL, '2026-05-08 15:06:17'),
(4, 'karl', '908990-890-09', 3, '2026-05-12', '20:21:00', 120, 12, 'confirmed', 'Study', '2026-05-12 12:22:06');

-- --------------------------------------------------------

--
-- Table structure for table `soft_balance_entries`
--

CREATE TABLE `soft_balance_entries` (
  `id` int(11) NOT NULL,
  `balance_date` date NOT NULL,
  `period` varchar(2) NOT NULL,
  `total_revenue` decimal(12,2) NOT NULL,
  `total_expenses` decimal(12,2) NOT NULL,
  `net_balance` decimal(12,2) NOT NULL,
  `notes` text DEFAULT NULL,
  `generated_by` int(11) NOT NULL,
  `generated_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `soft_balance_entries`
--

INSERT INTO `soft_balance_entries` (`id`, `balance_date`, `period`, `total_revenue`, `total_expenses`, `net_balance`, `notes`, `generated_by`, `generated_at`) VALUES
(1, '2026-05-08', 'AM', 1172.94, 0.00, 1172.94, 'smoke', 2, '2026-05-08 14:42:25'),
(2, '2026-05-08', 'AM', 1706.76, 10.00, 1696.76, 'smoke', 2, '2026-05-08 15:02:46'),
(3, '2026-05-08', 'AM', 1706.76, 20.00, 1686.76, 'smoke', 2, '2026-05-08 15:06:16'),
(4, '2026-05-08', 'AM', 1706.76, 240.00, 1466.76, 'NA', 2, '2026-05-08 15:10:24'),
(5, '2026-05-12', 'PM', 1846.29, 0.00, 1846.29, 'TESTING\n', 2, '2026-05-12 07:52:27'),
(6, '2026-05-12', 'PM', 1846.29, 540.00, 1306.29, 'PMPMMM', 2, '2026-05-12 08:37:31'),
(7, '2026-05-12', 'AM', 3397.90, 540.00, 2857.90, 'pmgets', 2, '2026-05-12 08:40:57'),
(8, '2026-05-12', 'AM', 3397.90, 1030.00, 2367.90, 'soft balancing for todayts 5/12/26 AM', 2, '2026-05-12 12:26:04'),
(9, '2026-05-18', 'AM', 0.00, 0.00, 0.00, 'trying\n', 2, '2026-05-18 04:55:59');

-- --------------------------------------------------------

--
-- Table structure for table `space_price_history`
--

CREATE TABLE `space_price_history` (
  `id` int(11) NOT NULL,
  `space_type_id` int(11) NOT NULL,
  `old_price` decimal(10,4) DEFAULT NULL,
  `new_price` decimal(10,4) NOT NULL,
  `changed_at` datetime NOT NULL,
  `changed_by_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `space_price_history`
--

INSERT INTO `space_price_history` (`id`, `space_type_id`, `old_price`, `new_price`, `changed_at`, `changed_by_id`) VALUES
(1, 3, 4.1667, 5.0000, '2026-05-13 13:55:59', 2),
(2, 3, 5.0000, 4.1667, '2026-05-15 08:01:07', 2);

-- --------------------------------------------------------

--
-- Table structure for table `space_types`
--

CREATE TABLE `space_types` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `rate_per_minute` decimal(10,4) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `capacity` int(11) DEFAULT NULL,
  `qr_token` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `space_types`
--

INSERT INTO `space_types` (`id`, `name`, `rate_per_minute`, `description`, `capacity`, `qr_token`) VALUES
(1, 'Regular Lounge', 0.1667, NULL, 30, NULL),
(2, 'Premium Lounge', 0.3333, NULL, 30, NULL),
(3, 'Boardroom', 4.1667, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `staff_attendance`
--

CREATE TABLE `staff_attendance` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `time_in` datetime NOT NULL,
  `time_out` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `staff_attendance`
--

INSERT INTO `staff_attendance` (`id`, `user_id`, `time_in`, `time_out`) VALUES
(2, 2, '2026-04-28 11:41:47', '2026-04-28 13:26:58'),
(4, 2, '2026-04-28 13:27:17', '2026-04-28 13:45:43'),
(6, 2, '2026-04-28 13:50:46', '2026-04-28 14:03:21'),
(8, 2, '2026-04-28 14:04:53', '2026-04-28 14:20:56'),
(9, 2, '2026-04-29 13:48:36', '2026-04-29 14:19:05'),
(10, 2, '2026-04-29 14:19:07', '2026-04-29 14:19:12'),
(11, 2, '2026-04-29 14:19:37', '2026-04-29 14:21:27'),
(13, 2, '2026-05-01 14:17:39', '2026-05-01 14:32:41'),
(15, 2, '2026-05-06 13:48:01', NULL),
(16, 2, '2026-05-07 12:49:33', '2026-05-07 13:10:51'),
(19, 2, '2026-05-07 13:11:33', '2026-05-07 13:11:55'),
(20, 2, '2026-05-08 11:57:41', NULL),
(21, 2, '2026-05-08 11:59:56', NULL),
(23, 2, '2026-05-08 14:44:22', '2026-05-08 14:57:53'),
(25, 2, '2026-05-08 14:58:06', '2026-05-08 15:05:38'),
(26, 2, '2026-05-08 15:05:44', '2026-05-08 15:06:18'),
(28, 2, '2026-05-08 15:06:46', '2026-05-08 15:13:04'),
(30, 2, '2026-05-10 08:12:04', NULL),
(31, 2, '2026-05-10 08:12:31', NULL),
(32, 2, '2026-05-10 08:15:28', NULL),
(33, 2, '2026-05-10 08:52:53', NULL),
(34, 2, '2026-05-10 09:27:49', '2026-05-10 09:51:59'),
(35, 2, '2026-05-10 10:05:06', NULL),
(36, 2, '2026-05-10 10:05:07', NULL),
(37, 2, '2026-05-10 10:11:24', NULL),
(38, 2, '2026-05-10 10:11:26', '2026-05-10 10:18:01'),
(39, 2, '2026-05-10 10:18:30', NULL),
(40, 2, '2026-05-12 07:09:24', NULL),
(41, 2, '2026-05-12 07:25:36', NULL),
(42, 2, '2026-05-12 07:25:41', '2026-05-12 07:38:52'),
(43, 2, '2026-05-12 07:38:59', NULL),
(44, 2, '2026-05-12 08:00:29', '2026-05-12 08:01:05'),
(45, 10, '2026-05-12 08:01:08', '2026-05-12 08:26:18'),
(46, 2, '2026-05-12 08:10:41', NULL),
(47, 2, '2026-05-12 08:30:39', NULL),
(48, 2, '2026-05-12 12:16:02', '2026-05-12 12:44:10'),
(49, 2, '2026-05-12 12:42:48', NULL),
(50, 10, '2026-05-12 12:44:15', '2026-05-12 13:07:04'),
(51, 2, '2026-05-12 13:07:12', '2026-05-12 13:09:59'),
(52, 2, '2026-05-13 13:23:03', NULL),
(53, 10, '2026-05-13 13:30:05', '2026-05-13 14:16:59'),
(54, 2, '2026-05-13 13:44:05', '2026-05-13 14:21:45'),
(55, 2, '2026-05-13 14:21:49', '2026-05-13 14:24:59'),
(56, 2, '2026-05-13 14:28:09', '2026-05-13 14:28:22'),
(57, 2, '2026-05-14 07:29:28', NULL),
(58, 2, '2026-05-14 08:00:05', '2026-05-14 08:00:38'),
(59, 10, '2026-05-14 08:00:19', '2026-05-14 08:00:32'),
(60, 10, '2026-05-14 08:00:42', '2026-05-14 08:40:19'),
(61, 2, '2026-05-14 08:40:24', NULL),
(62, 2, '2026-05-15 08:00:39', NULL),
(63, 2, '2026-05-15 09:57:54', NULL),
(64, 2, '2026-05-15 09:58:26', NULL),
(65, 2, '2026-05-15 12:06:40', '2026-05-15 12:16:32'),
(66, 10, '2026-05-15 12:16:36', NULL),
(67, 2, '2026-05-17 13:32:09', NULL),
(68, 2, '2026-05-18 04:34:10', NULL),
(69, 2, '2026-05-18 04:37:25', NULL),
(70, 2, '2026-05-18 05:03:40', NULL),
(71, 2, '2026-05-18 05:09:46', NULL),
(72, 2, '2026-05-18 05:16:45', NULL),
(73, 2, '2026-05-18 05:18:55', NULL),
(74, 2, '2026-05-18 05:23:31', NULL),
(75, 2, '2026-05-18 05:23:32', '2026-05-18 05:31:05'),
(76, 2, '2026-05-18 05:56:42', '2026-05-18 05:58:40'),
(77, 10, '2026-05-18 05:57:51', '2026-05-18 05:58:27'),
(78, 11, '2026-05-18 05:58:54', '2026-05-18 05:59:02');

-- --------------------------------------------------------

--
-- Table structure for table `staff_performance_logs`
--

CREATE TABLE `staff_performance_logs` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `shift_date` date NOT NULL,
  `orders_handled` int(11) NOT NULL,
  `avg_order_minutes` decimal(8,2) NOT NULL,
  `sessions_managed` int(11) NOT NULL,
  `upsell_count` int(11) NOT NULL,
  `admin_note` text DEFAULT NULL,
  `score` decimal(10,2) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `customers_served` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `staff_performance_logs`
--

INSERT INTO `staff_performance_logs` (`id`, `user_id`, `shift_date`, `orders_handled`, `avg_order_minutes`, `sessions_managed`, `upsell_count`, `admin_note`, `score`, `created_at`, `customers_served`) VALUES
(1, 2, '2026-05-08', 1, 1.00, 1, 0, 'smoke', 2.90, '2026-05-08 14:42:25', 0),
(2, 2, '2026-05-08', 1, 1.00, 1, 0, 'smoke', 2.90, '2026-05-08 15:02:49', 0),
(3, 2, '2026-05-08', 1, 1.00, 1, 0, 'smoke', 2.90, '2026-05-08 15:06:17', 0),
(4, 10, '2026-05-12', 0, 0.00, 0, 0, 'testing', 9.00, '2026-05-12 08:38:41', 9);

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `id` int(11) NOT NULL,
  `session_id` int(11) NOT NULL,
  `time_bill` decimal(10,2) NOT NULL,
  `food_bill` decimal(10,2) NOT NULL,
  `total_bill` decimal(10,2) NOT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`id`, `session_id`, `time_bill`, `food_bill`, `total_bill`, `created_at`) VALUES
(1, 1, 26.06, 855.00, 881.06, '2026-04-28 12:06:59'),
(2, 2, 14.40, 0.00, 14.40, '2026-04-28 12:17:41'),
(3, 3, 0.06, 0.00, 0.06, '2026-04-28 13:34:09'),
(4, 4, 0.31, 0.00, 0.31, '2026-04-28 14:02:48'),
(5, 5, 0.36, 275.00, 275.36, '2026-04-28 14:04:46'),
(6, 6, 6.04, 435.00, 441.04, '2026-04-29 14:49:19'),
(7, 7, 9.25, 185.00, 194.25, '2026-05-06 14:16:49'),
(8, 8, 5.24, 325.00, 330.24, '2026-05-07 13:10:26'),
(9, 10, 43.16, 420.00, 463.16, '2026-05-08 12:13:08'),
(10, 9, 44.78, 665.00, 709.78, '2026-05-08 12:13:11'),
(11, 11, 3.82, 530.00, 533.82, '2026-05-08 14:57:23'),
(12, 12, 28.40, 0.00, 28.40, '2026-05-10 09:51:31'),
(13, 13, 901.29, 945.00, 1846.29, '2026-05-12 07:10:12'),
(14, 14, 11.61, 1540.00, 1551.61, '2026-05-12 08:39:30'),
(15, 17, 195.03, 250.00, 445.03, '2026-05-18 05:30:28');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(20) NOT NULL,
  `job_role` varchar(50) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `failed_login_attempts` int(11) DEFAULT 0,
  `locked_until` datetime DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `password_changed_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `full_name`, `username`, `password`, `role`, `job_role`, `created_at`, `failed_login_attempts`, `locked_until`, `last_login`, `password_changed_at`) VALUES
(2, 'Admin', 'admin', '$2b$12$Rk8S8nplZcMI2JCikbSV/OhKjkE5sIm7WbR1Bn6GHqCGZ.1i5VE32', 'admin', 'admin', '2026-04-28 11:41:20', 0, NULL, '2026-05-18 05:56:42', '2026-05-15 17:34:35'),
(10, 'carl', 'carl', '$2b$12$X5Ap8AvVyR0ohrMjMT1WK..rCJK98tWj32ZE0pE5AGdSzVsxxLh9G', 'staff', 'cashier', '2026-05-12 08:01:02', 0, NULL, '2026-05-18 05:57:51', '2026-05-15 17:34:35'),
(11, 'paula', 'paula', '$2b$12$wXaqErhCJDhofhbrFCb.iekRvHXs4RCngXB/jSOLVjfc4Pr6wDiWW', 'staff', 'cook', '2026-05-18 05:57:28', 0, NULL, '2026-05-18 05:58:54', '2026-05-18 05:57:28');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `boardroom_bookings`
--
ALTER TABLE `boardroom_bookings`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `customer_sessions`
--
ALTER TABLE `customer_sessions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `space_type_id` (`space_type_id`);

--
-- Indexes for table `daily_sales_reports`
--
ALTER TABLE `daily_sales_reports`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `report_date` (`report_date`),
  ADD KEY `generated_by` (`generated_by`);

--
-- Indexes for table `departments`
--
ALTER TABLE `departments`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `expenses`
--
ALTER TABLE `expenses`
  ADD PRIMARY KEY (`id`),
  ADD KEY `logged_by` (`logged_by`);

--
-- Indexes for table `finance_budgets`
--
ALTER TABLE `finance_budgets`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `finance_transactions`
--
ALTER TABLE `finance_transactions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `budget_id` (`budget_id`);

--
-- Indexes for table `ideas`
--
ALTER TABLE `ideas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `department_id` (`department_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `idea_votes`
--
ALTER TABLE `idea_votes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idea_id` (`idea_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `inventory_items`
--
ALTER TABLE `inventory_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `menu_item_id` (`menu_item_id`);

--
-- Indexes for table `inventory_logs`
--
ALTER TABLE `inventory_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `inventory_item_id` (`inventory_item_id`),
  ADD KEY `changed_by` (`changed_by`);

--
-- Indexes for table `lounge_bookings`
--
ALTER TABLE `lounge_bookings`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `menu_items`
--
ALTER TABLE `menu_items`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `customer_session_id` (`customer_session_id`),
  ADD KEY `handled_by` (`handled_by`);

--
-- Indexes for table `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `menu_item_id` (`menu_item_id`);

--
-- Indexes for table `receivables`
--
ALTER TABLE `receivables`
  ADD PRIMARY KEY (`id`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `session_id` (`session_id`);

--
-- Indexes for table `reservations`
--
ALTER TABLE `reservations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `space_type_id` (`space_type_id`);

--
-- Indexes for table `soft_balance_entries`
--
ALTER TABLE `soft_balance_entries`
  ADD PRIMARY KEY (`id`),
  ADD KEY `generated_by` (`generated_by`),
  ADD KEY `ix_soft_balance_entries_balance_date` (`balance_date`);

--
-- Indexes for table `space_price_history`
--
ALTER TABLE `space_price_history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `space_type_id` (`space_type_id`),
  ADD KEY `changed_by_id` (`changed_by_id`);

--
-- Indexes for table `space_types`
--
ALTER TABLE `space_types`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD UNIQUE KEY `qr_token` (`qr_token`);

--
-- Indexes for table `staff_attendance`
--
ALTER TABLE `staff_attendance`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `staff_performance_logs`
--
ALTER TABLE `staff_performance_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `session_id` (`session_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `boardroom_bookings`
--
ALTER TABLE `boardroom_bookings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `customer_sessions`
--
ALTER TABLE `customer_sessions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `daily_sales_reports`
--
ALTER TABLE `daily_sales_reports`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `departments`
--
ALTER TABLE `departments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `expenses`
--
ALTER TABLE `expenses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `finance_budgets`
--
ALTER TABLE `finance_budgets`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `finance_transactions`
--
ALTER TABLE `finance_transactions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `ideas`
--
ALTER TABLE `ideas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `idea_votes`
--
ALTER TABLE `idea_votes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `inventory_items`
--
ALTER TABLE `inventory_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `inventory_logs`
--
ALTER TABLE `inventory_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `lounge_bookings`
--
ALTER TABLE `lounge_bookings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `menu_items`
--
ALTER TABLE `menu_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=78;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `order_items`
--
ALTER TABLE `order_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

--
-- AUTO_INCREMENT for table `receivables`
--
ALTER TABLE `receivables`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `reservations`
--
ALTER TABLE `reservations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `soft_balance_entries`
--
ALTER TABLE `soft_balance_entries`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `space_price_history`
--
ALTER TABLE `space_price_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `space_types`
--
ALTER TABLE `space_types`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `staff_attendance`
--
ALTER TABLE `staff_attendance`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=79;

--
-- AUTO_INCREMENT for table `staff_performance_logs`
--
ALTER TABLE `staff_performance_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `customer_sessions`
--
ALTER TABLE `customer_sessions`
  ADD CONSTRAINT `customer_sessions_ibfk_1` FOREIGN KEY (`space_type_id`) REFERENCES `space_types` (`id`);

--
-- Constraints for table `daily_sales_reports`
--
ALTER TABLE `daily_sales_reports`
  ADD CONSTRAINT `daily_sales_reports_ibfk_1` FOREIGN KEY (`generated_by`) REFERENCES `users` (`id`);

--
-- Constraints for table `expenses`
--
ALTER TABLE `expenses`
  ADD CONSTRAINT `expenses_ibfk_1` FOREIGN KEY (`logged_by`) REFERENCES `users` (`id`);

--
-- Constraints for table `finance_transactions`
--
ALTER TABLE `finance_transactions`
  ADD CONSTRAINT `finance_transactions_ibfk_1` FOREIGN KEY (`budget_id`) REFERENCES `finance_budgets` (`id`);

--
-- Constraints for table `ideas`
--
ALTER TABLE `ideas`
  ADD CONSTRAINT `ideas_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`),
  ADD CONSTRAINT `ideas_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `idea_votes`
--
ALTER TABLE `idea_votes`
  ADD CONSTRAINT `idea_votes_ibfk_1` FOREIGN KEY (`idea_id`) REFERENCES `ideas` (`id`),
  ADD CONSTRAINT `idea_votes_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `inventory_items`
--
ALTER TABLE `inventory_items`
  ADD CONSTRAINT `inventory_items_ibfk_1` FOREIGN KEY (`menu_item_id`) REFERENCES `menu_items` (`id`);

--
-- Constraints for table `inventory_logs`
--
ALTER TABLE `inventory_logs`
  ADD CONSTRAINT `inventory_logs_ibfk_1` FOREIGN KEY (`inventory_item_id`) REFERENCES `inventory_items` (`id`),
  ADD CONSTRAINT `inventory_logs_ibfk_2` FOREIGN KEY (`changed_by`) REFERENCES `users` (`id`);

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`customer_session_id`) REFERENCES `customer_sessions` (`id`),
  ADD CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`handled_by`) REFERENCES `users` (`id`);

--
-- Constraints for table `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`),
  ADD CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`menu_item_id`) REFERENCES `menu_items` (`id`);

--
-- Constraints for table `receivables`
--
ALTER TABLE `receivables`
  ADD CONSTRAINT `receivables_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `receivables_ibfk_2` FOREIGN KEY (`session_id`) REFERENCES `customer_sessions` (`id`);

--
-- Constraints for table `reservations`
--
ALTER TABLE `reservations`
  ADD CONSTRAINT `reservations_ibfk_1` FOREIGN KEY (`space_type_id`) REFERENCES `space_types` (`id`);

--
-- Constraints for table `soft_balance_entries`
--
ALTER TABLE `soft_balance_entries`
  ADD CONSTRAINT `soft_balance_entries_ibfk_1` FOREIGN KEY (`generated_by`) REFERENCES `users` (`id`);

--
-- Constraints for table `space_price_history`
--
ALTER TABLE `space_price_history`
  ADD CONSTRAINT `space_price_history_ibfk_1` FOREIGN KEY (`space_type_id`) REFERENCES `space_types` (`id`),
  ADD CONSTRAINT `space_price_history_ibfk_2` FOREIGN KEY (`changed_by_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `staff_attendance`
--
ALTER TABLE `staff_attendance`
  ADD CONSTRAINT `staff_attendance_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `staff_performance_logs`
--
ALTER TABLE `staff_performance_logs`
  ADD CONSTRAINT `staff_performance_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `transactions`
--
ALTER TABLE `transactions`
  ADD CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`session_id`) REFERENCES `customer_sessions` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
