object MovingAverage {



  def movingAvg(input: List[Double], windowSize: Int): List[Double] = {
    lazy val mAvg: LazyList[Double] = input.take(windowSize).sum #:: mAvg
      .zip(input.zip(input.drop(windowSize)))
      .map { case (sum, (previous, next)) => sum + next - previous }
    mAvg.map(_ / windowSize).toList
  }



  def main(args: Array[String]): Unit = {
    val input = List(0.8563, 0.8548, 0.8533, 0.8533, 0.8533, 0.8536, 0.8526,
      0.8519, 0.8539, 0.8489, 0.8489, 0.8489, 0.8501, 0.8457)

    val output = movingAvg(input, 3)
    println(output.mkString("\n"))
  }
}
