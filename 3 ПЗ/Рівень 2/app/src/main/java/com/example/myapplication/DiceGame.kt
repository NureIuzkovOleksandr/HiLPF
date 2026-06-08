package com.example.myapplication

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.myapplication.ui.theme.MyApplicationTheme
import kotlin.random.Random

class DiceGame(val numDice: Int = 3) {
    var player1Name = "Гравець 1"
    var player2Name = "Гравець 2"

    fun rollDice(): Pair<List<Int>, Int> {
        val rolls = List(numDice) { Random.nextInt(1, 7) }
        return Pair(rolls, rolls.sum())
    }

    fun setPlayerNames(player1: String, player2: String) {
        player1Name = player1
        player2Name = player2
    }
}

class DiceGameActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MyApplicationTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    DiceGameScreen(modifier = Modifier.padding(innerPadding))
                }
            }
        }
    }
}

@Composable
fun DiceGameScreen(modifier: Modifier = Modifier) {
    val game = remember { DiceGame(3) }
    var player1Name by remember { mutableStateOf("Гравець 1") }
    var player2Name by remember { mutableStateOf("Гравець 2") }
    
    var rolls1 by remember { mutableStateOf<List<Int>>(emptyList()) }
    var sum1 by remember { mutableIntStateOf(0) }
    var rolls2 by remember { mutableStateOf<List<Int>>(emptyList()) }
    var sum2 by remember { mutableIntStateOf(0) }
    var resultText by remember { mutableStateOf("") }

    val drawText = stringResource(R.string.result_draw)
    val winnerPattern = stringResource(R.string.result_winner)

    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(24.dp)
            .verticalScroll(rememberScrollState()),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        Text(
            text = stringResource(R.string.title_dice_game), 
            fontSize = 28.sp, 
            fontWeight = FontWeight.Bold,
            color = MaterialTheme.colorScheme.primary,
        )

        OutlinedTextField(
            value = player1Name,
            onValueChange = { player1Name = it },
            label = { Text(stringResource(R.string.player1_label)) },
            modifier = Modifier.fillMaxWidth(),
            singleLine = true,
        )

        OutlinedTextField(
            value = player2Name,
            onValueChange = { player2Name = it },
            label = { Text(stringResource(R.string.player2_label)) },
            modifier = Modifier.fillMaxWidth(),
            singleLine = true,
        )

        Button(
            onClick = {
                game.setPlayerNames(player1Name, player2Name)
                val (r1, s1) = game.rollDice()
                val (r2, s2) = game.rollDice()
                
                rolls1 = r1
                sum1 = s1
                rolls2 = r2
                sum2 = s2
                
                resultText = when {
                    sum1 > sum2 -> winnerPattern.format(player1Name)
                    sum2 > sum1 -> winnerPattern.format(player2Name)
                    else -> drawText
                }
            },
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp),
        ) {
            Text(stringResource(R.string.button_roll), fontSize = 18.sp)
        }

        if (rolls1.isNotEmpty() || rolls2.isNotEmpty()) {
            Spacer(modifier = Modifier.height(8.dp))
            
            PlayerResultCard(name = player1Name, rolls = rolls1, sum = sum1)
            PlayerResultCard(name = player2Name, rolls = rolls2, sum = sum2)

            Text(
                text = resultText,
                fontSize = 24.sp,
                fontWeight = FontWeight.ExtraBold,
                color = MaterialTheme.colorScheme.secondary,
                modifier = Modifier.padding(top = 16.dp),
            )
        }
    }
}

@Composable
fun PlayerResultCard(name: String, rolls: List<Int>, sum: Int) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceVariant,
        ),
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(text = name, fontWeight = FontWeight.Bold, fontSize = 20.sp)
            Text(text = stringResource(R.string.label_rolled, rolls.joinToString("  ")), fontSize = 16.sp)
            Text(text = stringResource(R.string.label_sum, sum), fontWeight = FontWeight.Medium, fontSize = 18.sp)
        }
    }
}
