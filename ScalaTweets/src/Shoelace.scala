object Shoelace {



  case class Point(x: Int, y: Int)

  def guess(polyPoints: List[Point]): Double = {
    val sum = polyPoints.zip(polyPoints.tail :+ polyPoints.head)
      .foldLeft(0.0) { case (t, (p1, p2)) =>
        t + (p1.x * p2.y) - (p1.y * p2.x)
      }
    math.abs(sum) / 2.0
  }



  def main(args: Array[String]): Unit = {
    println(guess(List(Point(3, 4), Point(5, 11), Point(12, 8), Point(9, 5), Point(5, 6))))
  }
}
