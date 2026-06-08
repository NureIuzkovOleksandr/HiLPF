package com.example.myapplication

import android.graphics.Color
import android.os.Bundle
import android.view.KeyEvent
import android.view.inputmethod.EditorInfo
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import java.util.Locale

class MainActivity : AppCompatActivity() {

    private lateinit var inputA: EditText
    private lateinit var inputB: EditText
    private lateinit var resultText: TextView
    private lateinit var divideButton: Button
    private lateinit var clearButton: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        inputA = findViewById(R.id.inputA)
        inputB = findViewById(R.id.inputB)
        resultText = findViewById(R.id.resultText)
        divideButton = findViewById(R.id.divideButton)
        clearButton = findViewById(R.id.clearButton)

        divideButton.setOnClickListener {
            calculateDivision()
        }

        clearButton.setOnClickListener {
            clearInputs()
        }

        // Handle Enter key on physical keyboard
        inputB.setOnKeyListener { _, keyCode, event ->
            if (keyCode == KeyEvent.KEYCODE_ENTER &&
                event.action == KeyEvent.ACTION_DOWN) {
                calculateDivision()
                true
            } else {
                false
            }
        }

        // Handle "Done" action on software keyboard
        inputB.setOnEditorActionListener { _, actionId, _ ->
            if (actionId == EditorInfo.IME_ACTION_DONE) {
                calculateDivision()
                true
            } else {
                false
            }
        }
    }

    private fun calculateDivision() {
        val aText = inputA.text.toString().trim()
        val bText = inputB.text.toString().trim()

        if (aText.isEmpty() || bText.isEmpty()) {
            Toast.makeText(
                this,
                getString(R.string.error_empty_inputs),
                Toast.LENGTH_SHORT
            ).show()
            return
        }

        try {
            val a = aText.toDouble()
            val b = bText.toDouble()

            if (b == 0.0) {
                Toast.makeText(
                    this,
                    getString(R.string.error_division_by_zero),
                    Toast.LENGTH_SHORT
                ).show()
                resultText.text = getString(R.string.text_error_division_by_zero)
                resultText.setTextColor(Color.RED)
                return
            }

            val result = a / b

            val formattedResult = if (result == result.toLong().toDouble()) {
                result.toLong().toString()
            } else {
                String.format(Locale.getDefault(), "%.4f", result)
            }

            resultText.text = getString(R.string.result_pattern, aText, bText, formattedResult)
            resultText.setTextColor(Color.BLACK)

            Toast.makeText(
                this,
                getString(R.string.toast_calculation_done),
                Toast.LENGTH_SHORT
            ).show()

        } catch (_: NumberFormatException) {
            Toast.makeText(
                this,
                getString(R.string.error_invalid_numbers),
                Toast.LENGTH_SHORT
            ).show()
            resultText.text = getString(R.string.text_error_format)
            resultText.setTextColor(Color.RED)
        }
    }

    private fun clearInputs() {
        inputA.text.clear()
        inputB.text.clear()
        resultText.text = getString(R.string.text_default_result)
        resultText.setTextColor(Color.BLACK)
        inputA.requestFocus()
    }
}
