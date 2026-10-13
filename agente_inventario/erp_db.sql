-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 20-09-2026 a las 22:37:22
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `erp_db`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(150) NOT NULL,
  `categoria` varchar(100) NOT NULL,
  `stock_actual` int(11) NOT NULL DEFAULT 0,
  `stock_minimo` int(11) NOT NULL DEFAULT 0,
  `stock_maximo` int(11) NOT NULL DEFAULT 0,
  `precio_compra` decimal(10,2) NOT NULL DEFAULT 0.00,
  `precio_venta` decimal(10,2) NOT NULL DEFAULT 0.00,
  `proveedor_id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id`, `nombre`, `categoria`, `stock_actual`, `stock_minimo`, `stock_maximo`, `precio_compra`, `precio_venta`, `proveedor_id`, `created_at`) VALUES
(1, 'Laptop Dell XPS 13', 'Computadoras', 0, 5, 15, 800.00, 1200.00, 1, '2026-09-19 16:35:31'),
(2, 'Mouse Logitech MX Master 3', 'Accesorios', 5, 8, 30, 50.00, 80.00, 2, '2026-09-19 16:35:31'),
(3, 'Teclado Mecánico RGB', 'Accesorios', 12, 5, 40, 80.00, 150.00, 3, '2026-09-19 16:35:31'),
(4, 'Monitor Samsung 27\"', 'Monitores', 25, 10, 40, 300.00, 450.00, 4, '2026-09-19 16:35:31'),
(5, 'SSD Western Digital 1TB', 'Almacenamiento', 3, 5, 25, 120.00, 200.00, 5, '2026-09-19 16:35:31'),
(6, 'Laptop HP 15\"', 'Computadoras', 40, 10, 50, 550.00, 800.00, 6, '2026-09-19 16:35:31'),
(7, 'Memoria RAM Kingston 16GB', 'Componentes', 4, 8, 35, 45.00, 75.00, 7, '2026-09-19 16:35:31'),
(8, 'Monitor Acer 24\"', 'Monitores', 18, 8, 30, 180.00, 280.00, 8, '2026-09-19 16:35:31');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedores`
--

CREATE TABLE `proveedores` (
  `id` int(11) NOT NULL,
  `nombre` varchar(150) NOT NULL,
  `contacto` varchar(100) DEFAULT NULL,
  `telefono` varchar(30) DEFAULT NULL,
  `tiempo_entrega_dias` int(11) NOT NULL DEFAULT 3,
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `proveedores`
--

INSERT INTO `proveedores` (`id`, `nombre`, `contacto`, `telefono`, `tiempo_entrega_dias`, `activo`, `created_at`) VALUES
(1, 'Dell Corp', 'Carlos Mendoza', '999111222', 5, 1, '2026-09-19 16:35:30'),
(2, 'Logitech Peru', 'Ana Torres', '999222333', 2, 1, '2026-09-19 16:35:30'),
(3, 'Corsair Distribution', 'Luis Ramirez', '999333444', 3, 1, '2026-09-19 16:35:30'),
(4, 'Samsung Electronics', 'Pedro Flores', '999444555', 4, 1, '2026-09-19 16:35:30'),
(5, 'Western Digital Peru', 'Maria Lopez', '999555666', 3, 1, '2026-09-19 16:35:30'),
(6, 'HP Distribution Peru', 'Jorge Castro', '999666777', 4, 1, '2026-09-19 16:35:30'),
(7, 'Kingston Technology', 'Daniel Ruiz', '999777888', 3, 1, '2026-09-19 16:35:30'),
(8, 'Acer Peru', 'Fernando Diaz', '999888999', 5, 1, '2026-09-19 16:35:30');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas`
--

CREATE TABLE `ventas` (
  `id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `fecha` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `ventas`
--

INSERT INTO `ventas` (`id`, `producto_id`, `cantidad`, `fecha`) VALUES
(1, 1, 2, '2026-08-21 10:15:00'),
(2, 1, 3, '2026-08-22 11:20:00'),
(3, 1, 2, '2026-08-23 14:10:00'),
(4, 1, 3, '2026-08-24 09:45:00'),
(5, 1, 2, '2026-08-25 15:30:00'),
(6, 1, 3, '2026-08-26 12:20:00'),
(7, 1, 2, '2026-08-27 13:15:00'),
(8, 1, 3, '2026-08-28 10:40:00'),
(9, 1, 2, '2026-08-29 16:10:00'),
(10, 1, 3, '2026-08-30 11:30:00'),
(11, 1, 2, '2026-08-31 14:20:00'),
(12, 1, 3, '2026-09-01 10:15:00'),
(13, 1, 2, '2026-09-02 13:40:00'),
(14, 1, 3, '2026-09-03 15:20:00'),
(15, 1, 2, '2026-09-04 11:10:00'),
(16, 1, 3, '2026-09-05 12:45:00'),
(17, 1, 2, '2026-09-06 14:30:00'),
(18, 1, 3, '2026-09-07 10:20:00'),
(19, 1, 2, '2026-09-08 13:15:00'),
(20, 1, 3, '2026-09-09 15:40:00'),
(21, 1, 2, '2026-09-10 11:30:00'),
(22, 1, 3, '2026-09-11 14:10:00'),
(23, 1, 2, '2026-09-12 10:45:00'),
(24, 1, 3, '2026-09-13 12:20:00'),
(25, 1, 2, '2026-09-14 15:10:00'),
(26, 1, 3, '2026-09-15 11:50:00'),
(27, 1, 2, '2026-09-16 13:30:00'),
(28, 1, 3, '2026-09-17 10:25:00'),
(29, 1, 2, '2026-09-18 14:15:00'),
(30, 1, 3, '2026-09-19 11:20:00'),
(31, 2, 3, '2026-08-21 10:20:00'),
(32, 2, 2, '2026-08-22 11:10:00'),
(33, 2, 4, '2026-08-23 13:20:00'),
(34, 2, 3, '2026-08-24 15:10:00'),
(35, 2, 2, '2026-08-25 09:40:00'),
(36, 2, 4, '2026-08-26 12:30:00'),
(37, 2, 3, '2026-08-27 14:20:00'),
(38, 2, 2, '2026-08-28 10:10:00'),
(39, 2, 4, '2026-08-29 13:40:00'),
(40, 2, 3, '2026-08-30 15:20:00'),
(41, 2, 2, '2026-08-31 11:10:00'),
(42, 2, 4, '2026-09-01 14:30:00'),
(43, 2, 3, '2026-09-02 10:20:00'),
(44, 2, 2, '2026-09-03 12:10:00'),
(45, 2, 4, '2026-09-04 15:40:00'),
(46, 2, 3, '2026-09-05 11:20:00'),
(47, 2, 2, '2026-09-06 13:30:00'),
(48, 2, 4, '2026-09-07 10:40:00'),
(49, 2, 3, '2026-09-08 14:10:00'),
(50, 2, 2, '2026-09-09 15:30:00'),
(51, 2, 4, '2026-09-10 11:40:00'),
(52, 2, 3, '2026-09-11 13:20:00'),
(53, 2, 2, '2026-09-12 10:30:00'),
(54, 2, 4, '2026-09-13 14:40:00'),
(55, 2, 3, '2026-09-14 11:15:00'),
(56, 2, 2, '2026-09-15 13:50:00'),
(57, 2, 4, '2026-09-16 10:25:00'),
(58, 2, 3, '2026-09-17 14:20:00'),
(59, 2, 2, '2026-09-18 11:30:00'),
(60, 2, 4, '2026-09-19 13:10:00'),
(61, 3, 2, '2026-08-21 10:30:00'),
(62, 3, 3, '2026-08-22 12:20:00'),
(63, 3, 2, '2026-08-23 14:10:00'),
(64, 3, 3, '2026-08-24 11:30:00'),
(65, 3, 2, '2026-08-25 15:20:00'),
(66, 3, 3, '2026-08-26 10:40:00'),
(67, 3, 2, '2026-08-27 13:30:00'),
(68, 3, 3, '2026-08-28 14:20:00'),
(69, 3, 2, '2026-08-29 11:10:00'),
(70, 3, 3, '2026-08-30 15:30:00'),
(71, 3, 2, '2026-08-31 12:20:00'),
(72, 3, 3, '2026-09-01 10:30:00'),
(73, 3, 2, '2026-09-02 14:10:00'),
(74, 3, 3, '2026-09-03 11:40:00'),
(75, 3, 2, '2026-09-04 15:20:00'),
(76, 3, 3, '2026-09-05 12:10:00'),
(77, 3, 2, '2026-09-06 14:40:00'),
(78, 3, 3, '2026-09-07 10:20:00'),
(79, 3, 2, '2026-09-08 13:10:00'),
(80, 3, 3, '2026-09-09 15:40:00'),
(81, 3, 2, '2026-09-10 11:30:00'),
(82, 3, 3, '2026-09-11 14:20:00'),
(83, 3, 2, '2026-09-12 10:40:00'),
(84, 3, 3, '2026-09-13 13:30:00'),
(85, 3, 2, '2026-09-14 15:10:00'),
(86, 3, 3, '2026-09-15 11:20:00'),
(87, 3, 2, '2026-09-16 14:30:00'),
(88, 3, 3, '2026-09-17 10:50:00'),
(89, 3, 2, '2026-09-18 13:40:00'),
(90, 3, 3, '2026-09-19 15:20:00'),
(91, 4, 1, '2026-08-22 11:30:00'),
(92, 4, 1, '2026-08-25 14:20:00'),
(93, 4, 1, '2026-08-29 10:40:00'),
(94, 4, 1, '2026-09-02 15:10:00'),
(95, 4, 1, '2026-09-06 12:30:00'),
(96, 4, 1, '2026-09-10 13:20:00'),
(97, 4, 1, '2026-09-14 11:40:00'),
(98, 4, 1, '2026-09-18 14:10:00'),
(99, 5, 1, '2026-08-21 10:10:00'),
(100, 5, 2, '2026-08-23 12:20:00'),
(101, 5, 1, '2026-08-25 14:30:00'),
(102, 5, 2, '2026-08-27 11:10:00'),
(103, 5, 1, '2026-08-29 15:20:00'),
(104, 5, 2, '2026-08-31 10:40:00'),
(105, 5, 1, '2026-09-02 13:30:00'),
(106, 5, 2, '2026-09-04 14:20:00'),
(107, 5, 1, '2026-09-06 11:30:00'),
(108, 5, 2, '2026-09-08 15:10:00'),
(109, 5, 1, '2026-09-10 12:40:00'),
(110, 5, 2, '2026-09-12 10:20:00'),
(111, 5, 1, '2026-09-14 14:30:00'),
(112, 5, 2, '2026-09-16 11:40:00'),
(113, 5, 1, '2026-09-18 13:20:00'),
(114, 6, 1, '2026-08-23 10:20:00'),
(115, 6, 1, '2026-08-28 13:10:00'),
(116, 6, 1, '2026-09-03 11:30:00'),
(117, 6, 1, '2026-09-08 15:20:00'),
(118, 6, 1, '2026-09-13 12:40:00'),
(119, 6, 1, '2026-09-18 14:30:00'),
(120, 7, 2, '2026-08-21 09:50:00'),
(121, 7, 3, '2026-08-22 11:30:00'),
(122, 7, 2, '2026-08-23 13:20:00'),
(123, 7, 3, '2026-08-24 15:10:00'),
(124, 7, 2, '2026-08-25 10:40:00'),
(125, 7, 3, '2026-08-26 12:20:00'),
(126, 7, 2, '2026-08-27 14:30:00'),
(127, 7, 3, '2026-08-28 11:10:00'),
(128, 7, 2, '2026-08-29 13:40:00'),
(129, 7, 3, '2026-08-30 15:20:00'),
(130, 7, 2, '2026-08-31 10:30:00'),
(131, 7, 3, '2026-09-01 12:40:00'),
(132, 7, 2, '2026-09-02 14:10:00'),
(133, 7, 3, '2026-09-03 11:20:00'),
(134, 7, 2, '2026-09-04 15:30:00'),
(135, 7, 3, '2026-09-05 10:50:00'),
(136, 7, 2, '2026-09-06 13:30:00'),
(137, 7, 3, '2026-09-07 14:20:00'),
(138, 7, 2, '2026-09-08 11:40:00'),
(139, 7, 3, '2026-09-09 15:10:00'),
(140, 7, 2, '2026-09-10 10:20:00'),
(141, 7, 3, '2026-09-11 12:30:00'),
(142, 7, 2, '2026-09-12 14:40:00'),
(143, 7, 3, '2026-09-13 11:10:00'),
(144, 7, 2, '2026-09-14 15:20:00'),
(145, 7, 3, '2026-09-15 10:30:00'),
(146, 7, 2, '2026-09-16 13:40:00'),
(147, 7, 3, '2026-09-17 14:10:00'),
(148, 7, 2, '2026-09-18 11:50:00'),
(149, 7, 3, '2026-09-19 15:00:00'),
(150, 8, 1, '2026-08-21 11:20:00'),
(151, 8, 1, '2026-08-23 13:40:00'),
(152, 8, 2, '2026-08-25 15:10:00'),
(153, 8, 1, '2026-08-27 10:30:00'),
(154, 8, 1, '2026-08-29 12:20:00'),
(155, 8, 2, '2026-08-31 14:40:00'),
(156, 8, 1, '2026-09-02 11:10:00'),
(157, 8, 1, '2026-09-04 13:30:00'),
(158, 8, 2, '2026-09-06 15:20:00'),
(159, 8, 1, '2026-09-08 10:40:00'),
(160, 8, 1, '2026-09-10 12:30:00'),
(161, 8, 2, '2026-09-12 14:20:00'),
(162, 8, 1, '2026-09-14 11:30:00'),
(163, 8, 1, '2026-09-16 13:40:00'),
(164, 8, 2, '2026-09-18 15:10:00');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_producto_proveedor` (`proveedor_id`);

--
-- Indices de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_ventas_producto_fecha` (`producto_id`,`fecha`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `ventas`
--
ALTER TABLE `ventas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=165;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `productos`
--
ALTER TABLE `productos`
  ADD CONSTRAINT `fk_producto_proveedor` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedores` (`id`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD CONSTRAINT `fk_venta_producto` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
